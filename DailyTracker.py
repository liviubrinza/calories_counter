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
                        'calories' : round(float(product.calories * float(quantity) / 100), 2),
                        'protein' : round(float(product.protein * float(quantity) / 100), 2),
                        'fats' : round(float(product.fats * float(quantity) / 100), 2),
                        'carbs' : round(float(product.carbs * float(quantity) / 100), 2)}
            print(new_entry)

            for entry in self.products:
                if entry['name'] == new_entry['name']:
                    entry['quantity'] = round(float(entry['quantity']) + float(new_entry['quantity']), 2)
                    entry['calories'] = round(float(entry['calories']) + float(new_entry['calories']), 2)
                    entry['protein'] = round(float(entry['protein']) + float(new_entry['protein']), 2)
                    entry['fats'] = round(float(entry['fats']) + float(new_entry['fats']), 2)
                    entry['carbs'] = round(float(entry['carbs']) + float(new_entry['carbs']), 2)
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
