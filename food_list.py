

import recipe
import json

class food_list:
    """
        A  class representing the json recipe DB.
    """
    def __init__(self):
        self._recipe_path = None
        self._ingredient_path = None
        self._recipe_list = []
        self._ingredient_list = []
        self.recipe_count = len(self._recipe_list)
        self.ingredient_count = len(self._ingredient_list)

    def store_food_list(self):
        json.dump(self._recipe_list, open(self._recipe_path, 'w'), sort_keys=True)

    def import_food_list(self):
        self._recipe_list = json.load(open(self._recipe_path))

    def add_recipe(self, recipe):
        self._recipe_list.append(recipe)
        self._update_recipe_count()

    def remove_recipe(self, recipe_id):
        pass

    def store_ingredient_list(self):
        json.dump(self._ingredient_list, open(self._recipe_path, 'w'), sort_keys=True)

    def set_db_path(self, path):
        self._recipe_path = path

    def get_db_path(self):
        return self._recipe_path

    def _update_recipe_count(self):
        self.recipe_count = len(self._recipe_list)

    def _update_ingredient_count(self):
        self.ingredient_count = len(self._ingredient_list)
