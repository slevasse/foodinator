import dataclasses
import json
import re
from datetime import date, datetime
#######################################
## Ingredient ##
#######################################
# TODO add a proper testbench for these classes
# TODO make a proper recipe cookbook for test purpose

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

    def to_txt(self, standard_value: int = None, comments: bool = True):
        if standard_value is None:
            txt = self.name + ": " + str(self.quantity) + " " + self.unit + "."
        else:
            txt = self.name + ": " + str(self.quantity) + " (" + str(standard_value) + ")" + self.unit + "."
        if comments:
            txt += "Comment: " + self.comment
        return txt

#######################################
## Recipe ##
#######################################


@dataclasses.dataclass
class Recipe:
    """ A  class representing a recipe. """
    name: str = None  # the recipe name
    prep_time: int = 0
    cook_time: int = 0
    serve: int = 0
    difficulty: str = None
    author: str = None
    last_updated: str = dataclasses.field(init=False, default=None)
    recipe_length: int = dataclasses.field(init=False, default=None)
    types: list[str] = dataclasses.field(default_factory=list)
    tags: list[str] = dataclasses.field(default_factory=list)
    ingredient_list: list[Ingredient] = dataclasses.field(default_factory=list)  # a list of ingredients ingredient
                                                                                 # name, (quantity, unit), type
                                                                                 # (meat, veg, spice, etc), season.
    instruction: str = None  # the cooking instruction

#
    def __post_init__(self):
        if self.name is None:
            self.name = "Insert name here"
        if self.author is None:
            self.author = "insert author name here"
        if self.difficulty is None:
            self.difficulty = Definitions().difficulties[0]
        self._update_meta()

    def _update_meta(self):
        self.recipe_length = len(self.ingredient_list)
        self.last_updated = str(date.today())

# Ingredients methods
    def append_ingredient(self, ingredient_obj_or_list):
        """ Add a single new ingredient or a list of new ingredient to the ingredient list. Type is protected"""
        if isinstance(ingredient_obj_or_list, list):
            for ing in ingredient_obj_or_list:
                self._append_single_ingredient(ing)
        else:
            self._append_single_ingredient(ingredient_obj_or_list)
        self._update_meta()

    def _append_single_ingredient(self, ingredient):
        if isinstance(ingredient, Ingredient):
            self.ingredient_list.append(ingredient)
        elif isinstance(ingredient, dict):
            temp = Ingredient()
            temp.from_dict(ingredient)
            self.ingredient_list.append(temp)
        else:
            raise TypeError('Expected class Ingredient or dicted ingredient, got ', type(ingredient))

    def remove_ingredient(self, ingredient_name_or_obj_or_list):
        """ Remove an ingredient from the ingredient list. Type is either an ingredient object or a string with the full
         name of the object"""
        if isinstance(ingredient_name_or_obj_or_list, list):
            for ing in ingredient_name_or_obj_or_list:
                self._remove_single_ingredient(ing)
        else:
            self._remove_single_ingredient(ingredient_name_or_obj_or_list)
        self._update_meta()

    def _remove_single_ingredient(self, ing_or_name):
        if isinstance(ing_or_name, Ingredient):
            self.ingredient_list.remove(ing_or_name)
        elif isinstance(ing_or_name, str):
            for ingredient in self.ingredient_list:
                if ing_or_name.lower() == ingredient.name.lower():
                    self.ingredient_list.remove(ingredient)
        else:
            raise TypeError('Expected class Ingredient or string, got ', type(ing_or_name))

# Type methods
    def append_recipe_type(self, recipe_type_or_list):
        """ Add a single new type or a list of new types to the type list. Type is protected"""
        if isinstance(recipe_type_or_list, list):
            for types in recipe_type_or_list:
                self._append_single_recipe_type(types)
        else:
            self._append_single_recipe_type(recipe_type_or_list)

    def remove_recipe_type(self, recipe_type_or_list):
        """ Remove a type from the type list. Variable type is a string with the full name of the object"""
        if isinstance(recipe_type_or_list, list):
            for types in recipe_type_or_list:
                self._remove_single_recipe_type(types)
        else:
            self._remove_single_recipe_type(recipe_type_or_list)

    def _append_single_recipe_type(self, recipe_type: str):
        if isinstance(recipe_type, str):
            self.types.append(recipe_type)
        else:
            raise TypeError('Expected class string, got ', type(recipe_type))

    def _remove_single_recipe_type(self, recipe_type: str):
        if isinstance(recipe_type, str):
            self.types.remove(recipe_type)
        else:
            raise TypeError('Expected class string, got ', type(recipe_type))

# Tags methods
    def append_recipe_tag(self, recipe_tag_or_list):
        """ Add a single new type or a list of new types to the type list. Type is protected"""
        if isinstance(recipe_tag_or_list, list):
            for tags in recipe_tag_or_list:
                self._append_single_recipe_tag(tags)
        else:
            self._append_single_recipe_tag(recipe_tag_or_list)

    def remove_recipe_tag(self, recipe_tag_or_list):
        """ Remove a type from the type list. Variable type is a string with the full name of the object"""
        if isinstance(recipe_tag_or_list, list):
            for tags in recipe_tag_or_list:
                self._remove_single_recipe_tag(tags)
        else:
            self._remove_single_recipe_tag(recipe_tag_or_list)

    def _append_single_recipe_tag(self, recipe_tag: str):
        if isinstance(recipe_tag, str):
            self.tags.append(recipe_tag)
        else:
            raise TypeError('Expected class string, got ', type(recipe_tag))

    def _remove_single_recipe_tag(self, recipe_tag: str):
        if isinstance(recipe_tag, str):
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
        self.prep_time = recipe_dict['prep_time']
        self.cook_time = recipe_dict['cook_time']
        self.serve = recipe_dict['serve']
        # clear existing
        self.types = []
        self.tags = []
        self.ingredient_list = []
        self.append_recipe_type(recipe_dict['types'])
        self.append_recipe_tag(recipe_dict['tags'])
        self.append_ingredient(recipe_dict['ingredient_list'])
        self.instruction = recipe_dict['instruction']
        self.difficulty = recipe_dict['difficulty']
        self.author = recipe_dict['author']
        self.last_updated = recipe_dict['last_updated']
        self.recipe_length = recipe_dict['recipe_length']

    def to_txt(self, comments: bool = True):
        txt = "--------------------\n"
        txt += self.name + "\n"
        txt += "--------------------\n"
        txt += "\n"
        txt += "Author: " + self.author + "\n"
        txt += "Difficulty: " + self.difficulty + "\n"
        txt += "Preparation time: " + str(self.prep_time) + " minutes \n"
        txt += "Cooking time: " + str(self.cook_time) + " minutes \n"
        txt += "Total time: " + str(self.cook_time + self.prep_time) + " minutes \n"
        txt += "Serve: " + str(self.serve) + " serving \n"
        txt += "Types: "
        txt += ', '.join(self.types)
        txt += "\n"
        txt += "Tags: "
        txt += ', '.join(self.tags)
        txt += "\n"
        txt += "\n"
        txt += "--------------------\n"
        txt += "Ingredients:\n"
        txt += "--------------------\n"
        for ing in self.ingredient_list:
            txt += "    -"
            txt += ing.to_txt(comments=comments)
            txt += "\n"
        txt += "------------------------------------------------------------\n"
        txt += "\n"
        return txt

#######################################
## Recipe ##
#######################################


@dataclasses.dataclass
class RecipeBook:
    """ A  class representing a recipe Book. """
    name: str = ""  # the name of the book
    path: str = ""  # The path of the book
    recipe_count: int = dataclasses.field(init=False, default=None)  # how many recipes are currently in the book
    last_updated: str = dataclasses.field(init=False, default=None)  # When was the last change to the book
    auto_save: bool = False  # does the book autosave (after every change to the class)?
    auto_backup: bool = True  # does the book makes automatic backup of the main book (in case of corruption or
                              # loss of data) Only if autosave is on.
    backup_interval: int = 5  # After how many changes do we backup ?
    backup_cnt: int = dataclasses.field(init=False, default=0)
    backup_history_length: int = 5  # how many backup file do we keep ? (rolling buffer type)
    recipe_list: list[Recipe] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self._update_meta()

    def __len__(self):
        return len(self.recipe_list)

    def _update_meta(self):
        self.recipe_count = len(self.recipe_list)
        self.last_updated = str(date.today())
        self.sort_recipes_alphabetically()

    def open(self, path):
        self.from_file(path)
        self.path = path

    @property
    def longest(self):
        duration = 0
        for recipe in self.recipe_list:
            total = recipe.cook_time + recipe.prep_time
            if total > duration:
                duration = total
        return duration

# add and remove recipes
    def _append_single_recipe(self, recipe):
        if isinstance(recipe, Recipe):
            self.recipe_list.append(recipe)
        elif type(recipe) == dict:
            temp = Recipe()
            temp.from_dict(recipe)
            self.recipe_list.append(temp)
        else:
            raise TypeError('Expected class Recipe or dict, got ', type(recipe))

    # TODO add check for if recipe name already exist
    def append(self, recipe_or_list, auto_save: bool = True):
        if isinstance(recipe_or_list, list):
            for recipe in recipe_or_list:
                self._append_single_recipe(recipe)
        else:
            self._append_single_recipe(recipe_or_list)
        self._update_meta()
        if auto_save:
            self._auto_save()

    def remove_recipe(self, recipe_name_or_obj_or_list):
        """ Remove an ingredient from the ingredient list. Type is either an ingredient object or a string with the full
         name of the object"""
        if isinstance(recipe_name_or_obj_or_list, list):
            for recipe in recipe_name_or_obj_or_list:
                self._remove_single_recipe(recipe)
        else:
            self._remove_single_recipe(recipe_name_or_obj_or_list)
        self._update_meta()
        self._auto_save()

    def _remove_single_recipe(self, recipe_or_name):
        if isinstance(recipe_or_name, Recipe):
            self.recipe_list.remove(recipe_or_name)
        elif type(recipe_or_name) == str:
            for recipe in self.recipe_list:
                if recipe_or_name.lower() == recipe.name.lower():
                    self.recipe_list.remove(recipe)
        else:
            raise TypeError('Expected class Recipe or string, got ', type(recipe_or_name))

# save and load the book
    @property
    def dict(self):
        return dataclasses.asdict(self)

    def from_dict(self, recipe_book_dict: dict):
        self.name = recipe_book_dict['name']
        self.path = recipe_book_dict['path']
        self.last_updated = recipe_book_dict['last_updated']
        self.recipe_count = recipe_book_dict['recipe_count']
        self.auto_save = recipe_book_dict['auto_save']
        self.auto_backup = recipe_book_dict['auto_backup']
        self.backup_interval = recipe_book_dict['backup_interval']
        self.backup_cnt = recipe_book_dict['backup_cnt']
        self.backup_history_length = recipe_book_dict['backup_history_length']
        self.recipe_list = []
        self.append(recipe_book_dict['recipe_list'], auto_save=False)

    def from_file(self, filepath: str = None):
        if filepath is None:
            path = self.path
        else:
            if filepath.endswith(Definitions().cookbook_file_extention):
                path = filepath
            else:
                raise TypeError("Provided file type is not " + Definitions().cookbook_file_extention)
        with open(path, "r") as read_file:
            self.from_dict(json.load(read_file))

    def to_file(self, filepath: str = None):
        if filepath is None:
            path = self.path
        else:
            if filepath.endswith(Definitions().cookbook_file_extention):
                path = filepath
            else:
                raise TypeError("Provided file type is not " + Definitions().cookbook_file_extention)
        with open(path, 'w') as outfile:
            json.dump(self.dict, outfile, sort_keys=False, indent=4)

    def _auto_save(self):
        if self.auto_save:
            if self.auto_backup:  # if we have backup enabled
                self.backup_cnt += 1
                if self.backup_cnt == self.backup_interval:  # do we need to do a backup ?
                    self.backup_cnt = 0
                    backup_name = self.path + self.name  + "_" + str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S")) + "_backup.json"
                    self.to_file(filepath = backup_name)
            self.to_file()

# find recipes in the cookbook
# make lists of all
    def find_unique_attributes(self, recipe_list: list) -> tuple:
        # TODO see how to improve even more the speed
        dif_set = set()
        name_set = set()
        author_set = set()
        tag_set = set()
        type_set = set()
        ingredient_name_set = set()
        ingredient_type_set = set()
        ingredient_season_set = set()
        for recipe in recipe_list:
            name_set.add(recipe.name)
            author_set.add(recipe.author)
            dif_set.add(recipe.difficulty)
            tag_set.update(recipe.tags)
            type_set.update(recipe.types)
            for val in recipe.ingredient_list:
                ingredient_name_set.add(val.name)
                ingredient_type_set.add(val.type)
                ingredient_season_set.add(val.season)

        return name_set, author_set, dif_set, tag_set, type_set, ingredient_name_set, ingredient_type_set, ingredient_season_set

    def find(self, search_form: list) -> list:
        method_library = {"recipe_name": self.check_recipe_name,
                          "recipe_tag": self.check_recipe_tag,
                          "recipe_type": self.check_recipe_type,
                          "recipe_author": self.check_recipe_author,
                          "recipe_duration": self.check_recipe_duration,
                          "recipe_difficulty": self.check_recipe_difficulty,
                          "ingredient_name": self.check_recipe_ingredient_name,
                          "ingredient_type": self.check_recipe_ingredient_type,
                          "ingredient_season": self.check_recipe_ingredient_season}
        result = []
        test = False
        for recipe in self.recipe_list:
            for form in search_form:
                test = method_library[form['search_mode']](form['key'], recipe)
                if not test:
                    break  # if we get there, this recipe is not matching all criteria and we can move on
            if test:
                result.append(recipe)
        return result

    def check_recipe_name(self, key: str, recipe: Recipe) -> bool:
        if re.search(key, recipe.name, re.IGNORECASE):
            return True
        return False

    def check_recipe_author(self, key: str, recipe: Recipe) -> bool:
        if re.search(key, recipe.author, re.IGNORECASE):
            return True
        return False

    def check_recipe_duration(self, key: str, recipe: Recipe) -> bool:
        if (recipe.prep_time + recipe.cook_time) <= int(key):
            return True
        return False

    def check_recipe_difficulty(self, key: str, recipe: Recipe) -> bool:
        if re.search(key, recipe.difficulty, re.IGNORECASE):
            return True
        return False

    def check_recipe_type(self, key: str, recipe: Recipe) -> bool:
        for typ in recipe.types:
            if re.search(key, typ, re.IGNORECASE):
                return True
        return False

    def check_recipe_tag(self, key: str, recipe: Recipe) -> bool:
        for tag in recipe.tags:
            if re.search(key, tag, re.IGNORECASE):
                return True
        return False

    def check_recipe_ingredient_name(self, key: str, recipe: Recipe) -> bool:
        for ingredient in recipe.ingredient_list:
            if re.search(key, ingredient.name, re.IGNORECASE):
                return True
        return False

    def check_recipe_ingredient_type(self, key: str, recipe: Recipe) -> bool:
        for ingredient in recipe.ingredient_list:
            if re.search(key, ingredient.type, re.IGNORECASE):
                return True
        return False

    def check_recipe_ingredient_season(self, key: str, recipe: Recipe) -> bool:
        for ingredient in recipe.ingredient_list:
            if re.search(key, ingredient.season, re.IGNORECASE):
                return True
        return False

    def sort_recipes_alphabetically(self, reverse=False):
        """Sort the recipes in alphabetical order based on their name. If the optional parameter 'reverse' is set to
        True, the list will be sorted in anti-alphabetical order."""
        self.recipe_list.sort(key=lambda x: x.name.lower(), reverse=reverse)

#######################################
## Definitions ##
#######################################


@dataclasses.dataclass(frozen=True)
class Definitions:
    cookbook_file_extention: str = dataclasses.field(default=('.cookbook'))
    difficulties: list[str] = dataclasses.field(default=("I'm too young to die",
                                                          "Hurt me plenty",
                                                          "Ultra-Violence",
                                                          "Nightmare",
                                                          "Ultra-Nightmare"))
    tags: list[str] = dataclasses.field(default=("Vegetarian",
                                                 "Vegan",
                                                 "Burger",
                                                 "Baby",
                                                 "High protein",
                                                 "Gluten free",
                                                 "Meat",
                                                 "Fish",
                                                 "Cold",
                                                 "Hot",
                                                 "Take away"))
    units: list[str] = dataclasses.field(default=("Piece",
                                                  "Clove",
                                                  "Leaf",
                                                  "milli Litre (mL)",
                                                  "Litre (L)",
                                                  "Gram (m)",
                                                  "kilo Gram (kg)",
                                                  "Table spoon",
                                                  "Tea spoon"))
    types: list[str] = dataclasses.field(default=("Breakfast",
                                                  "Main",
                                                  "Dessert",
                                                  "Fika",
                                                  "Starter",
                                                  "Juice",
                                                  "Smoothie",
                                                  "Soup"))
