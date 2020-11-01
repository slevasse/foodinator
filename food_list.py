

import recipe
import json
import os.path


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

    def import_recipe_list(self):
        # check if the path exist
        if not(os.path.isfile(self._recipe_path)):
            # if it does not exist we create it
            with open(self._recipe_path, 'w') as fp:
                pass
            # close it
            fp.close()
        else:
            # we try to import the file
            try:
                self._recipe_list = json.load(open(self._recipe_path))
            except json.decoder.JSONDecodeError:
                print("Food list is empty or invalid")

    def import_ingredient_list(self):
        # check if the path exist
        if not(os.path.isfile(self._ingredient_path)):
            # if it does not exist we create it
            with open(self._ingredient_path, 'w') as fp:
                pass
            # close it
            fp.close()
        else:
            # we try to import
            try:
                self._ingredient_list = json.load(open(self._ingredient_path))
            except json.decoder.JSONDecodeError:
                print("Ingredient list is empty or invalid")

    def add_recipe(self, recipe):
        self._recipe_list.append(recipe)
        self._update_recipe_count()

    def add_ingredient(self, ingredient):
        self._ingredient_list.append(ingredient)
        self._update_ingredient_count()

    def remove_recipe(self, recipe_id):
        pass

    def store_ingredient_list(self):
        json.dump(self._ingredient_list, open(self._recipe_path, 'w'), sort_keys=True)

    def set_recipe_db_path(self, path):
        self._recipe_path = path

    def get_recipe_db_path(self):
        return self._recipe_path

    def set_ingredient_db_path(self, path):
        self._ingredient_path = path

    def get_ingredient_db_path(self):
        return self._ingredient_path

    def _update_recipe_count(self):
        self.recipe_count = len(self._recipe_list)

    def _update_ingredient_count(self):
        self.ingredient_count = len(self._ingredient_list)

    def check_if_ingredient_exist(self, ingredient_name):
        for ingredient in self._ingredient_list:
            if ingredient_name == ingredient.name:
                return True
        return False
