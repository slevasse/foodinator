class recipe_defs:
    def __init__(self):
      self.tags = ["Vegetarian",
                   "Vegan",
                   "Burger",
                   "Baby",
                   "High protein",
                   "Gluten free",
                   "Meat",
                   "Fish",
                   "Cold",
                   "Hot",
                   "Take away"]

      self.types = ["Breakfast",
                    "Main",
                    "Dessert",
                    "Fika",
                    "Starter",
                    "Juice",
                    "Smoothie",
                    "Soup"]


class ingredient_def:
    def __init__(self):
      self.seasons = ["Spring",
                      "Autumn",
                      "Summer",
                      "Winter",
                      "Not applicable"]

      self.types = ["Fruit",
                    "Root-Vegy",
                    "Salad-Vegy",
                    "Stem-Vegy",
                    "Sea-Vegy",
                    "Spice",
                    "Condiment",
                    "Dairy",
                    "Canned",
                    "Dry",
                    "Fish",
                    "poultry",
                    "Beef",
                    "Pig",
                    "Wild meat",
                    "Other"]

      self.units = ["Piece",
                    "Clove",
                    "Leaf",
                    "milli Litre (mL)",
                    "Litre (L)",
                    "Gram (m)",
                    "kilo Gram (kg)",
                    "Table spoon",
                    "Tea spoon"]


class search_configuration_def:
    def __init__(self, person_count, day_count, lunch_and_dinner, types, tags):
        self.configuration = {'person count': person_count,
                              'day count': day_count,
                              'lunch and dinner': lunch_and_dinner,
                              'type': types,
                              'tags': tags}
