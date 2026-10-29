import os
from datetime import date
import Persistence

class DailyTracker:

    labels = ['Protein', 'Fats', 'Carbs']
    colors = ["#3B82F6", "#F59E0B", "#EF4444"]
    # the current day is kept in <project_root>/persisted/<username>_daily.json, so a restart does not lose it
    # daily stats are saved in <project_root>/persisted/<username>_stats/<YYYY_MM>/<DD>.txt
    # when the date changes, the tracked day is saved to the stats and the tracker starts a new empty day
    persist_dir = Persistence.PERSIST_DIR

    def __init__(self, productsHandler, username, dishesHandler=None):
        self.percentage_values = [0, 0, 0]
        self.total_calories = 0
        self.total_protein = 0
        self.total_fats = 0
        self.total_carbs = 0
        self.products = []
        self.date = date.today()   # the day the tracked products belong to
        self.productsHandler = productsHandler
        self.dishesHandler = dishesHandler
        self.stats_path = os.path.join(DailyTracker.persist_dir, username + "_stats")
        self.daily_filename = os.path.join(DailyTracker.persist_dir, username + "_daily.json")

        os.makedirs(self.stats_path, exist_ok=True)
        self._read_json_data()
        self.check_day_rollover()

    def _read_json_data(self):
        data = Persistence.load_json(self.daily_filename, default={})
        self.products = data.get('products', [])
        # files saved before the date was tracked are treated as today, so they roll over on the next day
        if 'date' in data:
            self.date = date.fromisoformat(data['date'])
        self._recalculate_daily_macros()

    def _write_json_data(self):
        # totals are derived from the products, so they are stored for readability and recomputed on load
        Persistence.save_json(self.daily_filename, {'date': self.date.isoformat(),
                                                    'products': self.products,
                                                    'total_calories': round(self.total_calories, 2),
                                                    'total_protein': round(self.total_protein, 2),
                                                    'total_fats': round(self.total_fats, 2),
                                                    'total_carbs': round(self.total_carbs, 2),
                                                    'percentages': {'protein': self.percentage_values[0],
                                                                    'fats': self.percentage_values[1],
                                                                    'carbs': self.percentage_values[2]}
                                                    })

    def check_day_rollover(self):
        # called at startup and before every tracker request, so a missed midnight (server off) is still handled
        if self.date == date.today():
            return

        if self.products:
            self.save_daily_stats()
        self.reset_day()

    def save_daily_stats(self):
        # stats are filed under the tracked day, not the moment of saving (matters when saving after midnight)
        month_path = os.path.join(self.stats_path, self.date.strftime("%Y_%m"))
        os.makedirs(month_path, exist_ok=True)

        file_path = os.path.join(month_path, self.date.strftime("%d") + ".txt")
        
        with open(file_path, 'w') as f:
            f.write("Total calories: " + str(self.total_calories) + "\n")
            f.write("\tProtein: " + str(self.total_protein) + "(" + str(self.percentage_values[0]) + "%)\n")
            f.write("\tFats: " + str(self.total_fats) +  "(" + str(self.percentage_values[1]) + "%)\n")
            f.write("\tCarbs: " + str(self.total_carbs) +  "(" + str(self.percentage_values[2]) + "%)\n")
            f.write("=========================\n")
            f.write("Name \t\t Quantity \t Calories \t Protein \t Fats \t Carbs\n")
            for product in self.products:
                f.write(product['name'] + " \t\t " 
                        + str(product['quantity']) + " \t\t " 
                        + str(product['calories']) + " \t\t " 
                        + str(product['protein']) + " \t\t " 
                        + str(product['fats']) + " \t\t " 
                        + str(product['carbs']) + "\n")

    def get_saved_stats(self):
        # reads back only the totals header of every saved day, newest first; the product lines are skipped
        days = []
        for month_dir in os.listdir(self.stats_path):
            month_path = os.path.join(self.stats_path, month_dir)
            if not os.path.isdir(month_path):
                continue
            for day_file in os.listdir(month_path):
                try:
                    year, month = month_dir.split("_")
                    day_date = date(int(year), int(month), int(day_file.removesuffix(".txt")))
                except ValueError:
                    continue

                totals = {}
                with open(os.path.join(month_path, day_file)) as f:
                    for line in f:
                        if line.startswith("="):
                            break
                        # "Total calories: 1646.8" or "\tProtein: 168.82(41.0%)"
                        key, _, value = line.strip().partition(":")
                        totals[key] = round(float(value.split("(")[0]), 2)

                days.append({'date': day_date,
                             'calories': totals.get('Total calories', 0),
                             'protein': totals.get('Protein', 0),
                             'fats': totals.get('Fats', 0),
                             'carbs': totals.get('Carbs', 0)})

        days.sort(key=lambda day: day['date'], reverse=True)
        return days

    def add_product(self, name, quantity):
        product = self._get_item_by_name(name)
        quantity = int(quantity)

        if product:
            retVal = False
            new_entry = {'name' : product.name, 
                        'quantity' : quantity,
                        'calories' : round(float(product.calories * float(quantity) / 100), 2),
                        'protein' : round(float(product.protein * float(quantity) / 100), 2),
                        'fats' : round(float(product.fats * float(quantity) / 100), 2),
                        'carbs' : round(float(product.carbs * float(quantity) / 100), 2)}

            for entry in self.products:
                if entry['name'] == new_entry['name']:
                    entry['quantity'] = round(float(entry['quantity']) + float(new_entry['quantity']), 2)
                    entry['calories'] = round(float(entry['calories']) + float(new_entry['calories']), 2)
                    entry['protein'] = round(float(entry['protein']) + float(new_entry['protein']), 2)
                    entry['fats'] = round(float(entry['fats']) + float(new_entry['fats']), 2)
                    entry['carbs'] = round(float(entry['carbs']) + float(new_entry['carbs']), 2)
                    retVal = True
                    break

            if not retVal:
                self.products.append(new_entry)
        
            self._recalculate_daily_macros()
            self._write_json_data()

    def remove_product(self, name):
        retVal = False
        for product in self.products:
            if product['name'] == name:
                self.products.remove(product)
                retVal = True
        self._recalculate_daily_macros()
        if retVal:
            self._write_json_data()
        return retVal

    def adjust_product_quantity(self, name, quantity):
        retVal = False

        for product in self.products:
            if product['name'] == name:
                product_data = self._get_item_by_name(name)
                if not product_data:
                    break

                product['quantity'] = round(float(quantity), 2)
                product['calories'] = round(float(product_data.calories * float(quantity) / 100), 2)
                product['protein'] = round(float(product_data.protein * float(quantity) / 100), 2)
                product['fats'] = round(float(product_data.fats * float(quantity) / 100), 2)
                product['carbs'] = round(float(product_data.carbs * float(quantity) / 100), 2)
                retVal = True

        self._recalculate_daily_macros()
        if retVal:
            self._write_json_data()
        return retVal

    def _get_item_by_name(self, name):
        # raw products first, then prepared dishes (both expose values per 100g)
        product = self.productsHandler.get_product_by_name(name)
        if not product and self.dishesHandler:
            product = self.dishesHandler.get_dish_by_name(name)
        return product

    def reset_day(self):
        self.percentage_values = [0, 0, 0]
        self.total_calories = 0
        self.total_protein = 0
        self.total_fats = 0
        self.total_carbs = 0
        self.products = []
        self.date = date.today()
        self._write_json_data()

    def _recalculate_daily_macros(self):
        self.total_calories = 0
        self.total_protein  = 0
        self.total_fats     = 0
        self.total_carbs    = 0

        for product in self.products:
            self.total_calories += product['calories']
            self.total_protein  += product['protein']
            self.total_fats     += product['fats']
            self.total_carbs    += product['carbs']

        # share of the daily calories coming from each macro, in percent (4 kcal/g protein and carbs, 9 kcal/g fats)
        self.percentage_values = [self._macro_percentage(self.total_protein, 4),
                                  self._macro_percentage(self.total_fats, 9),
                                  self._macro_percentage(self.total_carbs, 4)]

    def _macro_percentage(self, grams, kcal_per_gram):
        if self.total_calories <= 0:
            return 0

        percentage = kcal_per_gram * grams * 100 / self.total_calories
        rounded = round(percentage, 1)

        # a macro that is present should never show as 0%, so tiny values are bumped to the smallest step
        if percentage > 0 and rounded == 0:
            return 0.1
        return rounded