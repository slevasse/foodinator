from food_item_library.foodLibrary import FoodLibrary
from dataclasses import *
from foodClasses import *

import json

test_file = "recipe_list.json"

lib = FoodLibrary()
ing0 = Ingredient()
ing1 = Ingredient(0,0,lib[0])
ing2 = Ingredient(0,0,lib[30])
ing3 = Ingredient(0,0,lib[40])
ings = [ing1, ing2, ing3]


ing1_dict = ing1.dict
ing0.from_dict(ing1_dict)

rec = Recipe("hoy", 0, 12, 12, 1)

rec.append_ingredient(ing1)

rec.append_ingredient(ings)

rec.remove_ingredient(['apple', ing2])
rec.append_recipe_type(['main', 'breakfast'])
rec.append_recipe_tag(['cold', 'vegan'])
rec.remove_recipe_type(['main'])
rec.remove_recipe_tag(['vegan'])

auto_dict = rec.dict

rec2 = Recipe()
rec2.from_dict(auto_dict)
rec3 = Recipe("paota", 0, 12, 56, 1, ['hum'], ['drumm'])

book = RecipeBook()
book.append([rec,rec2])
book.name = "my_super_cookbook"
book._path = "cookbooks/"
book.to_file()
book.auto_save = True
book.append(rec3)
book.append(rec3)
book.append(rec3)
book.append(rec3)
book.append(rec3)
book_dicted = book.dict
new_book = RecipeBook()
new_book.from_dict(book_dicted)
new_book == book
book2 = RecipeBook()
book2.name = "my_super_cookbook"
book2._path = "cookbooks/"
book2.from_file()