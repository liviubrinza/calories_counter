
class Product:

    def __init__(self, name, calories, protein, fats, carbs):
        self.name = name
        self.calories = round(float(calories), 2)
        self.protein = round(float(protein), 2)
        self.fats = round(float(fats), 2)
        self.carbs = round(float(carbs), 2)

    def to_csv(self):
        return self.name + "," \
                + str(self.calories) + "," \
                + str(self.protein) + "," \
                + str(self.fats) + "," \
                + str(self.carbs)

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
                