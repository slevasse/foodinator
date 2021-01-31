import recipe
import json
import os.path
import logging
import copy
from PyQt5.QtWidgets import *
from ingredient import ingredient

class food_list:
    """
        A  class representing the json recipe DB.
    """
    def __init__(self):
        self._recipe_path = None
        self._recipe_list = []
        self.recipe_count = len(self._recipe_list)

#===============================================================================
# IOs
#================================
    def store_recipe_list(self):
        if len(self._recipe_list) > 0:
            dicted_recipe_list = []
            for rec in self._recipe_list:
                dicted_recipe_list.append(rec.dictify())
            dictified_recipe_list = {"recipe_list": dicted_recipe_list}
            # write to file
            with open(self._recipe_path, 'w') as outfile:
                json.dump(dictified_recipe_list, outfile,sort_keys=False, indent=4)

            outfile.close()
        else:
            logging.warning("Tried to write the recipe_list to file but list is empty.")

    def import_recipe_list(self):
        try:
            with open(self._recipe_path, "r") as read_file:
                # load the file as a dict
                data = json.load(read_file)
                # iterate through the dict
                for a_recipe in data["recipe_list"]:
                    # get the ingredients
                    ingredient_list = []
                    for a_ing in a_recipe["_ingredient_list"]:
                        ingredient_list.append(ingredient(a_ing["name"],
                                                        a_ing["quantity"],
                                                        a_ing["unit"],
                                                        a_ing["type"],
                                                        a_ing["season"],))
                                                        # write the new object list
                    self._recipe_list.append(recipe.recipe(a_recipe["_name"],
                                                           a_recipe["_id"],
                                                           a_recipe["_meta_data"],
                                                           ingredient_list,
                                                           a_recipe["_instruction"]))
                self.recipe_count = len(self._recipe_list)
                return (True, "")
        except FileNotFoundError:
            # if the file is not found
            # log that we could not find the file
            logging.error("IN IMPORT_RECIPE_LIST: The file countaining the recipes was not found, please check that : %s , is a correct path.", self._recipe_path)
            return (False, "The file: %s, was not found, please check that the file exist and try again.", self._recipe_path)
        except json.decoder.JSONDecodeError:
            # log that we could not find the file
            logging.error("IN IMPORT_RECIPE_LIST: The content of the file countaining the recipes is invalid, please check that the path and file content is correct and and try again.")
            return (False, "The content of the file countaining the recipes is invalid, please check that the path and file content is correct and and try again.")

#===============================================================================
# IOs
#================================
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
            self._recipe_list.append(copy.deepcopy(recipe))
            # increase the counter
            self._update_recipe_count()
            # write to file
            self.store_recipe_list()


    def remove_recipe(self, recipe_id):
        index = None
        for i in range(len(self._recipe_list)):
            if self._recipe_list[i]._id == recipe_id:
                index = i
        if not index is None:
            del self._recipe_list[index]



    def set_recipe_db_path(self, path):
        self._recipe_path = path

    def get_recipe_db_path(self):
        return self._recipe_path

    def _update_recipe_count(self):
        self.recipe_count = len(self._recipe_list)
