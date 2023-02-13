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
            self.products.append({'product': product, 'quantity': quantity})

    def remove_product(self, name):
        pass

    def adjust_product_quantity(self, name, quantity):
        pass
