import recipe
import json
import os.path
import logging


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

    def store_recipe_list(self):
        print("store function is not yet implemented")

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
                logging.error("Food list is empty or invalid")

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
                logging.error("Ingredient list is empty or invalid")

    def add_recipe(self, recipe):
        # check if recipe already exist
        if (False):
            pass
        # if not, then add it to the list
        else:
            if self.recipe_count > 0:
                # edit the recipe ID (plus 1)
                recipe._id = self._recipe_list[-1]._id + 1
            # add the recipe to the food list
            self._recipe_list.append(recipe)
            # increase the counter
            self._update_recipe_count()
            # write to file
            self.store_recipe_list()


    def add_ingredient(self, ingredient):
        self._ingredient_list.append(ingredient)
        self._update_ingredient_count()

    def remove_recipe(self, recipe_id):
        pass

    def store_ingredient_list(self):
        pass

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

    #===========================================================================
    # check if input and output files
    #================================
    def check_if_list_path_is_correct(self, path):
        if path.endswith('.json'):
            return True
        else:
            logging.error("The file provided is not a Json file.")
            return False
