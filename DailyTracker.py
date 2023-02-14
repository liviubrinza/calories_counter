from CsvReader import CsvReader

class DailyTracker:

    labels = ['Protein', 'Fats', 'Carbs']
    values = [0, 0, 0]
    colors = ["#1E81B0", "#DCE629", "#D93939"]

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
                product_data = self.csvReader.get_product_by_name(name)
                
                product['quantity'] = quantity
                product['calories'] = round(float(product_data.calories * float(quantity) / 100), 2)
                product['protein'] = round(float(product_data.protein * float(quantity) / 100), 2)
                product['fats'] = round(float(product_data.fats * float(quantity) / 100), 2)
                product['carbs'] = round(float(product_data.carbs * float(quantity) / 100), 2)
                retVal = True

        self._recalculate_daily_macros()
        return retVal

    def _recalculate_daily_macros(self):
        self.total_calories = 0
        self.total_protein  = 0
        self.total_fats     = 0
        self.total_carbs    = 0

        protein_percentage = 0
        fats_percentage    = 0
        carbs_percentage   = 0
        
        for product in self.products:
            self.total_calories += product['calories']
            self.total_protein  += product['protein']
            self.total_fats     += product['fats']
            self.total_carbs    += product['carbs']

        if self.total_calories > 0:
            protein_percentage = round(4 * self.total_protein / self.total_calories, 2)
            fats_percentage    = round(9 * self.total_fats / self.total_calories, 2)
            carbs_percentage   = round(4 * self.total_carbs / self.total_calories, 2)

        DailyTracker.values = [protein_percentage, fats_percentage, carbs_percentage]