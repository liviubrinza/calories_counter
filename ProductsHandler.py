import csv
from Product import Product

class ProductsHandler:
    filename = "products.csv"

    def __init__(self):
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
        
        self.products

    def get_products_list(self):
        return sorted(self.products, key=lambda x: x.name)


    def get_product_by_name(self, name):
        for product in self.products:
            if product.name == name:
                return product
        return None


    def add_new_product(self, new_product):
        if new_product.name and new_product.calories and new_product.protein and new_product.fats and new_product.carbs:     
            self.products.append(new_product)
            return True
        else:
            return False

    def remove_product(self, product_name):
        for product in self.products:
            if product.name == product_name:
                self.products.remove(product)
                print("[INFO] Product removed")
                return True
        print("[ERROR] Product not found to remove")
        return False

    def change_product(self, changed_product):
        for i in range(len(self.products)):
            if self.products[i].name == changed_product.name:
                self.products[i] = changed_product        
                return True
        return False