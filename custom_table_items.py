from PyQt5.QtWidgets import *
import ingredient
from recipe import recipe
from ingredient import ingredient
from all_definition import search_configuration_def
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

class search_configuration_table_item(QTableWidgetItem):
    def __init__(self, configuration):
        super().__init__()
        self.configuration = configuration
        self.setText(str(self.configuration.configuration['person count']))
