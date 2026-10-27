import math
import os
import Persistence
from Dish import Dish

class DishesHandler:
    # dishes are persisted in <project_root>/persisted/dishes.json and reloaded at startup
    filename = os.path.join(Persistence.PERSIST_DIR, "dishes.json")

    def __init__(self, productsHandler):
        self.dishes = []
        self.productsHandler = productsHandler
        self._read_json_data()

    def _read_json_data(self):
        self.dishes = [Dish.from_dict(entry) for entry in Persistence.load_json(DishesHandler.filename, default=[])]

    def _write_json_data(self):
        Persistence.save_json(DishesHandler.filename, [dish.to_dict() for dish in self.dishes])

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
        error = self._check_name(name)
        if error:
            return error

        entries, error = self._build_ingredients(name, ingredients)
        if error:
            return error

        self.dishes.append(Dish(name=name, ingredients=entries))
        self._write_json_data()
        return None

    def update_dish(self, original_name, name, ingredients):
        # replaces the ingredients of an existing dish (and renames it if the name changed)
        # returns None on success, an error message otherwise
        dish = self.get_dish_by_name(original_name)
        if not dish:
            return "Dish not found: " + original_name
        if name != original_name:
            error = self._check_name(name)
            if error:
                return error

        # ingredients whose product was removed in the meantime keep their saved values
        previous = {ingredient['name']: ingredient for ingredient in dish.ingredients}
        entries, error = self._build_ingredients(name, ingredients, previous)
        if error:
            return error

        self.dishes[self.dishes.index(dish)] = Dish(name=name, ingredients=entries)
        self._write_json_data()
        return None

    def _check_name(self, name):
        if not name:
            return "Dish name is missing"
        if self.get_dish_by_name(name):
            return "A dish with this name already exists: " + name
        if self.productsHandler.get_product_by_name(name):
            return "A product with this name already exists: " + name
        return None

    def _build_ingredients(self, name, ingredients, previous=None):
        # returns (entries, None) on success, (None, error message) otherwise
        previous = previous or {}

        # same product added more than once is merged into a single ingredient
        quantities = {}
        for product_name, quantity in ingredients:
            if not self.productsHandler.get_product_by_name(product_name) and product_name not in previous:
                return None, "Product not found: " + product_name
            try:
                quantity = float(quantity)
            except (TypeError, ValueError):
                return None, "Invalid quantity for: " + product_name
            if not math.isfinite(quantity) or quantity <= 0:
                return None, "Invalid quantity for: " + product_name
            quantities[product_name] = quantities.get(product_name, 0) + quantity

        if not quantities:
            return None, "Dish has no ingredients: " + name

        entries = []
        for product_name, quantity in quantities.items():
            product = self.productsHandler.get_product_by_name(product_name)
            if product:
                per_100g = {'calories': product.calories, 'protein': product.protein,
                            'fats': product.fats, 'carbs': product.carbs}
            else:
                # derive per 100g values from the previously saved ingredient
                old = previous[product_name]
                per_100g = {key: old[key] * 100 / old['quantity'] for key in ('calories', 'protein', 'fats', 'carbs')}
            entries.append({'name' : product_name,
                            'quantity' : round(quantity, 2),
                            'calories' : round(per_100g['calories'] * quantity / 100, 2),
                            'protein' : round(per_100g['protein'] * quantity / 100, 2),
                            'fats' : round(per_100g['fats'] * quantity / 100, 2),
                            'carbs' : round(per_100g['carbs'] * quantity / 100, 2)})

        return entries, None

    def remove_dish(self, dish_name):
        for dish in self.dishes:
            if dish.name == dish_name:
                self.dishes.remove(dish)
                self._write_json_data()
                return True
        print("[ERROR] Dish not found to remove: " + dish_name)
        return False
