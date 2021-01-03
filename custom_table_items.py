from PyQt5.QtWidgets import *
import ingredient
from recipe import recipe
from ingredient import ingredient
import logging

class recipe_table_item(QTableWidgetItem):
    def __init__(self, recipe):
        super().__init__()
        self.setText(recipe._name)
        self.recipe = recipe

class ingredient_table_item(QTableWidgetItem):
    def __init__(self, ing):
        super().__init__()
        self.setText(ing.name)
        self.ingredient = ing
