import csv
from Product import Product

class ProductsHandler:
    filename = "products.csv"
    fieldNames = ['Nume','Calorii','Proteine','Lipide','Carbohidrati']

    def __init__(self):
        self.products = []
        self._read_csv_data()

    def _read_csv_data(self):
        self.products = []

        with open(ProductsHandler.filename) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            line_count = 0

            for row in reader:
                if line_count > 0 and row:
                    product = Product(name=row[0],
                                      calories=round(float(row[1]), 2),
                                      protein=round(float(row[2]), 2),
                                      fats=round(float(row[3]), 2),
                                      carbs=round(float(row[4]), 2))
                    self.products.append(product)
                line_count += 1
            self.products = sorted(self.products, key=lambda x: x.name)

    def _write_csv_data(self):
        rows = []
        for product in self.products:
            rows.append(product.to_csv_dict())
       
        with open(ProductsHandler.filename, 'w', newline='') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=ProductsHandler.fieldNames)
            writer.writeheader()
            writer.writerows(rows)

    def get_products_list(self):
        return sorted(self.products, key=lambda x: x.name)

    def get_product_by_name(self, name):
        for product in self.products:
            if product.name == name:
                return product
        return None

    def add_new_product(self, new_product):
        if new_product.name and new_product.calories >= 0 and new_product.protein >= 0 and new_product.fats >= 0 and new_product.carbs >=0:     
            self.products.append(new_product)
            self._write_csv_data()
            return True
        else:
            print("[ERROR] Product not added: " + new_product.to_csv())
            return False

    def remove_product(self, product_name):
        for product in self.products:
            if product.name == product_name:
                self.products.remove(product)
                self._write_csv_data()
                return True
        print("[ERROR] Product not found to remove: " + product_name)
        return False

    def change_product(self, changed_product):
        for i in range(len(self.products)):
            if self.products[i].name == changed_product.name:
                self.products[i] = changed_product
                self._write_csv_data()        
                return True
        print("[ERROR] Product not changed: " + changed_product.name)
        return False