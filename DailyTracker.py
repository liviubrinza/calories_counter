from CsvReader import CsvReader

class DailyTracker:

    def __init__(self, csvReader):
        self.total_calories = 0
        self.total_protein = 0
        self.total_fats = 0
        self.total_carbs = 0
        self.csvReader = csvReader
        self.products = [self.csvReader.get_products_list()[0]]

    def add_product(self, quantity):
        pass

    def remove_product(self):
        pass

    def adjust_product_quantity(self, quantity):
        pass
