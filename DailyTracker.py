import os
from datetime import date

class DailyTracker:

    labels = ['Protein', 'Fats', 'Carbs']
    colors = ["#3B82F6", "#F59E0B", "#EF4444"]
    # daily stats are saved in <project_root>/persisted/<username>_stats/<YYYY_MM>/<DD>.txt
    persist_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persisted")

    def __init__(self, productsHandler, username, dishesHandler=None):
        self.percentage_values = [0, 0, 0]
        self.total_calories = 0
        self.total_protein = 0
        self.total_fats = 0
        self.total_carbs = 0
        self.products = []
        self.productsHandler = productsHandler
        self.dishesHandler = dishesHandler
        self.stats_path = os.path.join(DailyTracker.persist_dir, username + "_stats")

        os.makedirs(self.stats_path, exist_ok=True)

    def save_daily_stats(self):
        month_path = os.path.join(self.stats_path, date.today().strftime("%Y_%m"))
        os.makedirs(month_path, exist_ok=True)

        file_path = os.path.join(month_path, date.today().strftime("%d") + ".txt")
        
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

    def remove_product(self, name):
        retVal = False
        for product in self.products:
            if product['name'] == name:
                self.products.remove(product)
                retVal = True
        self._recalculate_daily_macros()
        return retVal

    def adjust_product_quantity(self, name, quantity):
        retVal = False

        for product in self.products:
            if product['name'] == name:
                product_data = self._get_item_by_name(name)
                if not product_data:
                    break

                product['quantity'] = quantity
                product['calories'] = round(float(product_data.calories * float(quantity) / 100), 2)
                product['protein'] = round(float(product_data.protein * float(quantity) / 100), 2)
                product['fats'] = round(float(product_data.fats * float(quantity) / 100), 2)
                product['carbs'] = round(float(product_data.carbs * float(quantity) / 100), 2)
                retVal = True

        self._recalculate_daily_macros()
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