
class Product:

    def __init__(self, name, calories, protein, fats, carbs):
        self.name = name
        self.calories = calories
        self.protein = protein
        self.fats = fats
        self.carbs = carbs

    def to_csv(self):
        return self.name + "," \
                + self.calories + "," \
                + self.protein + "," \
                + self.fats + "," \
                + self.carbs

    def __dict__(self):
        return {'product': {'name': self.name,
                            "calories": self.calories,
                            "protein": self.protein,
                            "fats": self.fats,
                            "carbs": self.carbs
                            }
                }