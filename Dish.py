
class Dish:

    def __init__(self, name, ingredients):
        # ingredients: list of dicts with name, quantity, calories, protein, fats, carbs (for the used quantity)
        self.name = name
        self.ingredients = ingredients

        self.total_quantity = round(sum(i['quantity'] for i in ingredients), 2)
        self.total_calories = round(sum(i['calories'] for i in ingredients), 2)
        self.total_protein = round(sum(i['protein'] for i in ingredients), 2)
        self.total_fats = round(sum(i['fats'] for i in ingredients), 2)
        self.total_carbs = round(sum(i['carbs'] for i in ingredients), 2)

        # values per 100g, same as Product, so the daily tracker can use a dish like any product
        self.calories = self._per_100g(self.total_calories)
        self.protein = self._per_100g(self.total_protein)
        self.fats = self._per_100g(self.total_fats)
        self.carbs = self._per_100g(self.total_carbs)

    def _per_100g(self, value):
        if self.total_quantity > 0:
            return round(value * 100 / self.total_quantity, 2)
        return 0
