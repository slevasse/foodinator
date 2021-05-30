from PyQt5.QtWidgets import *
from foodClasses import *


class RecipeTableItem(QTableWidgetItem):
    def __init__(self, recipe: Recipe):
        super().__init__()
        self.setText(recipe.name)
        self.recipe = recipe


class IngredientTableItem(QTableWidgetItem):
    def __init__(self, ingredient: Ingredient):
        super().__init__()
        self.setText(ingredient.food_item['Name'])
        self.ingredient = ingredient

