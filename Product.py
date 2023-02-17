
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
        return {'name': self.name,
                 'calories': self.calories,
                 'protein': self.protein,
                 'fats': self.fats,
                 'carbs': self.carbs
                }
    
    def to_csv_dict(self):
        return {'Nume': self.name,
                'Calorii': self.calories,
                'Proteine': self.protein,
                'Lipide': self.fats,
                'Carbohidrati': self.carbs
                }
                