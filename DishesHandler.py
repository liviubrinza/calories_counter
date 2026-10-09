import math
from Dish import Dish

class DishesHandler:
    # dishes are kept in memory only, a restart clears them

    def __init__(self, productsHandler):
        self.dishes = []
        self.productsHandler = productsHandler

    def get_dishes_list(self):
        return sorted(self.dishes, key=lambda x: x.name)

    def get_dish_by_name(self, name):
        for dish in self.dishes:
            if dish.name == name:
                return dish
        return None

    def add_new_dish(self, name, ingredients):
        # ingredients: list of (product_name, quantity) pairs
        # returns None on success, an error message otherwise
        if not name:
            return "Dish name is missing"
        if self.get_dish_by_name(name):
            return "A dish with this name already exists: " + name
        if self.productsHandler.get_product_by_name(name):
            return "A product with this name already exists: " + name

        # same product added more than once is merged into a single ingredient
        quantities = {}
        for product_name, quantity in ingredients:
            if not self.productsHandler.get_product_by_name(product_name):
                return "Product not found: " + product_name
            try:
                quantity = float(quantity)
            except (TypeError, ValueError):
                return "Invalid quantity for: " + product_name
            if not math.isfinite(quantity) or quantity <= 0:
                return "Invalid quantity for: " + product_name
            quantities[product_name] = quantities.get(product_name, 0) + quantity

        if not quantities:
            return "Dish has no ingredients: " + name

        entries = []
        for product_name, quantity in quantities.items():
            product = self.productsHandler.get_product_by_name(product_name)
            entries.append({'name' : product.name,
                            'quantity' : round(quantity, 2),
                            'calories' : round(product.calories * quantity / 100, 2),
                            'protein' : round(product.protein * quantity / 100, 2),
                            'fats' : round(product.fats * quantity / 100, 2),
                            'carbs' : round(product.carbs * quantity / 100, 2)})

        self.dishes.append(Dish(name=name, ingredients=entries))
        return None

    def remove_dish(self, dish_name):
        for dish in self.dishes:
            if dish.name == dish_name:
                self.dishes.remove(dish)
                return True
        print("[ERROR] Dish not found to remove: " + dish_name)
        return False
