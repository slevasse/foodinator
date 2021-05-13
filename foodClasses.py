import dataclasses

import json

from datetime import date, datetime
#######################################
## Ingredient ##
#######################################


@dataclasses.dataclass
class Ingredient:
    """ A  class representing an ingredient. """
    quantity: float = None
    unit: str = None
    food_item: dict = None
    comment: str = None

    @property
    def name(self):
        return self.food_item['Name']

    @property
    def type(self):
        return self.food_item['Type']

    @property
    def season(self):
        return self.food_item['Season']

    @property
    def dict(self):
        return dataclasses.asdict(self)

    def from_dict(self, dict_ingredient):
        self.quantity = dict_ingredient['quantity']
        self.unit = dict_ingredient['unit']
        self.food_item = dict_ingredient['food_item']
        self.comment = dict_ingredient['comment']

#######################################
## Recipe ##
#######################################


@dataclasses.dataclass
class Recipe:
    """ A  class representing a recipe. """
    name: str = None  # the recipe name
    id: int = None  # a unique ID for that recipe
    prep_time: int = None
    cook_time: int = None
    serve: int = None
    difficulty: str = None
    author: str = None
    last_updated: str = None
    recipe_length: int = None
    types: list[str] = dataclasses.field(default_factory=list)
    tags: list[str] = dataclasses.field(default_factory=list)
    ingredient_list: list[Ingredient] = dataclasses.field(default_factory=list)  # a list of ingredients ingredient name, (quantity, unit), type (meat, veg, spice, etc), season.
    instruction: str = None  # the instruction as a text, optional

#
    def _update_meta(self):
        self.recipe_length = len(self.ingredient_list)
        self.last_updated = str(date.today())

# Ingredients methods
    def append_ingredient(self, ingredient_obj_or_list):
        """ Add a single new ingredient or a list of new ingredient to the ingredient list. Type is protected"""
        if type(ingredient_obj_or_list) == list:
            for ing in ingredient_obj_or_list:
                self._append_single_ingredient(ing)
        else:
            self._append_single_ingredient(ingredient_obj_or_list)
        self._update_meta()

    def _append_single_ingredient(self, ingredient):
        if type(ingredient) == Ingredient:
            self.ingredient_list.append(ingredient)
        elif type(ingredient) == dict:
            temp = Ingredient()
            temp.from_dict(ingredient)
            self.ingredient_list.append(temp)
        else:
            raise TypeError('Expected class Ingredient or dicted ingredient, got ', type(ingredient))

    def remove_ingredient(self, ingredient_name_or_obj_or_list):
        """ Remove an ingredient from the ingredient list. Type is either an ingredient object or a string with the full name of the object"""
        if type(ingredient_name_or_obj_or_list) == list:
            for ing in ingredient_name_or_obj_or_list:
                self._remove_single_ingredient(ing)
        else:
            self._remove_single_ingredient(ingredient_name_or_obj_or_list)
        self._update_meta()

    def _remove_single_ingredient(self, ing_or_name):
        if type(ing_or_name) == Ingredient:
            self.ingredient_list.remove(ing_or_name)
        elif type(ing_or_name) == str:
            for ingredient in self.ingredient_list:
                if ing_or_name.lower() == ingredient.name.lower():
                    self.ingredient_list.remove(ingredient)
        else:
            raise TypeError('Expected class Ingredient or string, got ', type(ing_or_name))

# Type methods
    def append_recipe_type(self, recipe_type_or_list):
        """ Add a single new type or a list of new types to the type list. Type is protected"""
        if type(recipe_type_or_list) == list:
            for types in recipe_type_or_list:
                self._append_single_recipe_type(types)
        else:
            self._append_single_recipe_type(recipe_type_or_list)

    def remove_recipe_type(self, recipe_type_or_list):
        """ Remove a type from the type list. Variable type is a string with the full name of the object"""
        if type(recipe_type_or_list) == list:
            for types in recipe_type_or_list:
                self._remove_single_recipe_type(types)
        else:
            self._remove_single_recipe_type(recipe_type_or_list)

    def _append_single_recipe_type(self, recipe_type: str):
        if type(recipe_type) == str:
            self.types.append(recipe_type)
        else:
            raise TypeError('Expected class string, got ', type(recipe_type))

    def _remove_single_recipe_type(self, recipe_type: str):
        if type(recipe_type) == str:
            self.types.remove(recipe_type)
        else:
            raise TypeError('Expected class string, got ', type(recipe_type))

# Tags methods
    def append_recipe_tag(self, recipe_tag_or_list):
        """ Add a single new type or a list of new types to the type list. Type is protected"""
        if type(recipe_tag_or_list) == list:
            for tags in recipe_tag_or_list:
                self._append_single_recipe_tag(tags)
        else:
            self._append_single_recipe_tag(recipe_tag_or_list)

    def remove_recipe_tag(self, recipe_tag_or_list):
        """ Remove a type from the type list. Variable type is a string with the full name of the object"""
        if type(recipe_tag_or_list) == list:
            for tags in recipe_tag_or_list:
                self._remove_single_recipe_tag(tags)
        else:
            self._remove_single_recipe_tag(recipe_tag_or_list)

    def _append_single_recipe_tag(self, recipe_tag: str):
        if type(recipe_tag) == str:
            self.tags.append(recipe_tag)
        else:
            raise TypeError('Expected class string, got ', type(recipe_tag))

    def _remove_single_recipe_tag(self, recipe_tag: str):
        if type(recipe_tag) == str:
            self.tags.remove(recipe_tag)
        else:
            raise TypeError('Expected class string, got ', type(recipe_tag))

# IOs
    @property
    def dict(self):
        """Return a dict version of the class."""
        return dataclasses.asdict(self)

    def from_dict(self, recipe_dict):
        """Fill the class from a dict version of a similar class"""
        self.name = recipe_dict['name']
        self.id = recipe_dict['id']
        self.prep_time = recipe_dict['prep_time']
        self.cook_time = recipe_dict['cook_time']
        self.serve = recipe_dict['serve']
        self.append_recipe_type(recipe_dict['types'])
        self.append_recipe_tag(recipe_dict['tags'])
        self.append_ingredient(recipe_dict['ingredient_list'])
        self.instruction = recipe_dict['instruction']
        self.difficulty = recipe_dict['difficulty']
        self.author = recipe_dict['author']
        self.last_updated = recipe_dict['last_updated']
        self.recipe_length = recipe_dict['recipe_length']

#######################################
## Recipe ##
#######################################


@dataclasses.dataclass
class RecipeBook:
    """ A  class representing a recipe Book. """
    name: str = "default_cookbook_name"  # the name of the book
    _path: str = "/"  # The path of the book
    recipe_count: int = None  # how many recipes are currently in the book
    last_updated: str = None  # When was the last change to the book
    auto_save: bool = False  # does the book autosave (after every change to the class)?
    auto_backup: bool = True  # does the book makes automatic backup of the main book (in case of corruption or loss of data) Only if autosave is on.
    backup_interval: int = 5  # After how many changes do we backup ?
    backup_cnt: int = 0
    backup_history_length: int = 5  # how many backup file do we keep ? (rolling buffer type)
    recipe_list: list[Recipe] = dataclasses.field(default_factory=list)

#
    def __len__(self):
        return len(self.recipe_list)

    def _update_meta(self):
        self.recipe_count = len(self.recipe_list)
        self.last_updated = str(date.today())

# add and remove recipes
    def _append_single_recipe(self, recipe):
        if type(recipe) == Recipe:
            self.recipe_list.append(recipe)
        elif type(recipe) == dict:
            temp = Recipe()
            temp.from_dict(recipe)
            self.recipe_list.append(temp)
        else:
            raise TypeError('Expected class Recipe or dict, got ', type(recipe))

    def append(self, recipe_or_list, auto_save: bool = True):
        if type(recipe_or_list) == list:
            for recipe in recipe_or_list:
                self._append_single_recipe(recipe)
        else:
            self._append_single_recipe(recipe_or_list)
        self._update_meta()
        if auto_save:
            self._auto_save()

    def remove_recipe(self, recipe_name_or_obj_or_list):
        """ Remove an ingredient from the ingredient list. Type is either an ingredient object or a string with the full name of the object"""
        if type(recipe_name_or_obj_or_list) == list:
            for recipe in recipe_name_or_obj_or_list:
                self._remove_single_recipe(recipe)
        else:
            self._remove_single_recipe(recipe_name_or_obj_or_list)
        self._update_meta()
        self._auto_save()

    def _remove_single_recipe(self, recipe_or_name):
        if type(recipe_or_name) == Recipe:
            self.recipe_list.remove(recipe_or_name)
        elif type(recipe_or_name) == str:
            for recipe in self.recipe_list:
                if recipe_or_name.lower() == recipe.name.lower():
                    self.recipe_list.remove(recipe)
        else:
            raise TypeError('Expected class Ingredient or string, got ', type(recipe_or_name))

# save and load the book
    @property
    def dict(self):
        return dataclasses.asdict(self)

    def from_dict(self, recipe_book_dict):
        self.name = recipe_book_dict['name']
        self._path = recipe_book_dict['_path']
        self.last_updated = recipe_book_dict['last_updated']
        self.recipe_count = recipe_book_dict['recipe_count']
        self.auto_save = recipe_book_dict['auto_save']
        self.auto_backup = recipe_book_dict['auto_backup']
        self.backup_interval = recipe_book_dict['backup_interval']
        self.backup_cnt = recipe_book_dict['backup_cnt']
        self.backup_history_length = recipe_book_dict['backup_history_length']
        self.append(recipe_book_dict['recipe_list'], auto_save = False)

    def from_file(self, filepath: str = None):
        if filepath is None:
            path = self._path + self.name + "_cookBook.json"
        else:
            path = filepath
        with open(path, "r") as read_file:
            self.from_dict(json.load(read_file))

    def to_file(self, filepath: str = None):
        if filepath is None:
            path = self._path + self.name + "_cookBook.json"
        else:
            path = filepath
        with open(path, 'w') as outfile:
            json.dump(self.dict, outfile, sort_keys=False, indent=4)

    def _auto_save(self):
        if self.auto_save:
            if self.auto_backup:  # if we have backup enabled
                self.backup_cnt += 1
                if self.backup_cnt == self.backup_interval:  # do we need to do a backup ?
                    self.backup_cnt = 0
                    backup_name = self._path + self.name  + "_" + str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S")) + "_backup.json"
                    self.to_file(filepath = backup_name)
            self.to_file()
