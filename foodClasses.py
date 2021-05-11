import dataclasses

import copy


@dataclasses.dataclass
class Ingredient:
    """ A  class representing an ingredient. """
    name: str
    quantity: float
    unit: str
    type: str
    season: str


@dataclasses.dataclass
class Recipe:
    """ A  class representing a recipe. """
    name: str  # the name
    id: int
    meta_data: dataclasses.field(default_factory=dict)  # preptime, cooktime, serve N,
    ingredient_list: dataclasses.field(default_factory=list)  # a list of ingredients ingredient name, (quantity, unit), type (meat, veg, spice, etc), season.
    instruction: str  # the instruction as a text, optional

    def add_ingredient(self, ingredient_obj):
        self._ingredient_list.append(ingredient_obj)

    def remove_ingredient(self, ingredient_name):
        pass

    def add_tag(self, tag):
        self._tags.append(tag)

    def update_meta_data(self, preptime = 0, cooktime = 0, serve = 0, type = [], tags = []):
        self._meta_data['preptime'] = preptime
        self._meta_data['cooktime'] = cooktime
        self._meta_data['serve'] = serve
        self._meta_data['type'] = type
        self._meta_data['tags'] = tags

    def set_name(self, name):
        self._name = name

    def dictify(self):
        # make a deepcopy of original object
        temp_recipe = copy.deepcopy(self)
        # convert the list of ingredient to a dict
        dict_ingredient_list = []
        for ing in temp_recipe._ingredient_list:
            dict_ingredient_list.append(ing.__dict__)
        # convert the rest of the object
        temp_dict = temp_recipe.__dict__
        # replace the ingredient list by the dict ingredient list
        temp_dict['_ingredient_list'] = dict_ingredient_list
        return temp_dict

    def print_recipe(self):
        print(self._name)
        print(self._id)
        print(self._meta_data)
        print(self._ingredient_list)
        print(self._instruction)

    def clear_recipe(self):
        self._name = None
        self._id = 0
        self._meta_data = {'preptime':0, 'cooktime':0, 'serve':0}
        self._ingredient_list = []
        self._instruction = ''

