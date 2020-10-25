


import ingredient
import json

class recipe:
    """
        A  class representing a recipe.
    """
    def __init__(self, name = None,
                 id = 0,
                 meta_data = {'preptime':0, 'cooktime':0, 'serve':0},
                 ingredient_list = [],
                 instruction = '',
                 tags = []):
        self._name = name  # the name
        self._id = id
        self._meta_data = meta_data  # preptime, cooktime, serve N,
        self._ingredient_list = ingredient_list  # a list of ingredients ingredient name, (quantity, unit), type (meat, veg, spice, etc), season.
        self._instruction = instruction  # the instruction as a text, optional
        self._tags = tags  # a list of tags relating the recipe

    def add_ingredient(self, ingredient_obj):
        self._ingredient_list.append(ingredient_obj)

    def remove_ingredient(self, ingredient_name):
        pass

    def add_tag(self, tag):
        self._tags.append(tag)

    def update_meta_data(self, preptime = 0, cooktime = 0, serve = 0):
        self._meta_data['preptime'] = preptime
        self._meta_data['cooktime'] = cooktime
        self._meta_data['serve'] = serve

    def remove_tag(self, tag):
        pass

    def set_name(self, name):
        self._name = path

    def get_db_path(self):
        return self._recipe_path
