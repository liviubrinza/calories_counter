from CsvReader import CsvReader

class DailyTracker:

    def __init__(self, csvReader):
        self.total_calories = 0
        self.total_protein = 0
        self.total_fats = 0
        self.total_carbs = 0
        self.csvReader = csvReader
        self.products = []

    def add_product(self, name, quantity):
        product = self.csvReader.get_product_by_name(name)

        if product:
            new_entry = {'name' : product.name, 
                        'quantity' : quantity,
                        'calories' : float(product.calories * float(quantity) / 100),
                        'protein' : float(product.protein * float(quantity) / 100),
                        'fats' : float(product.fats * float(quantity) / 100),
                        'carbs' : float(product.carbs * float(quantity) / 100)}
            print(new_entry)

            for entry in self.products:
                if entry['name'] == new_entry['name']:
                    entry['quantity'] = float(entry['quantity']) + float(new_entry['quantity'])
                    entry['calories'] = float(entry['calories']) + float(new_entry['calories'])
                    entry['protein'] = float(entry['protein']) + float(new_entry['protein'])
                    entry['fats'] = float(entry['fats']) + float(new_entry['fats'])
                    entry['carbs'] = float(entry['carbs']) + float(new_entry['carbs'])
                    return
            
            self.products.append(new_entry)

    def remove_product(self, name):
        for product in self.products:
            if product['name'] == name:
                self.products.remove(product)
                return True
        return False

    def adjust_product_quantity(self, name, quantity):
        pass
