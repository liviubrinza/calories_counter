import csv
from Product import Product

class CsvReader:
        filename = "products.csv"

        def __init__(self):
            self.products = []

            with open(CsvReader.filename) as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                line_count = 0

                for row in reader:
                    if line_count > 0 and row:
                        print(row)
                        product = Product(name=row[0],
                                          calories=row[1],
                                          protein=row[2],
                                          fats=row[3],
                                          carbs=row[4])
                        self.products.append(product)
                    line_count += 1

        def get_products_list(self):
            return self.products
