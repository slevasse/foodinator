from food_item_library.foodLibrary import FoodLibrary
from random import *
import string
from foodClasses import *
import timeit
from datetime import date, datetime
import json

# code snippet to be executed only once


def random_string(str_size):
    return ''.join(choice(string.ascii_letters) for x in range(str_size))

def rand_ingredient():
    units = ["Unit", 'Gram', 'Litre']
    lib = FoodLibrary()
    ing = Ingredient(randint(1,10), choice(units), choice(lib), random_string(randint(1,20)))
    return ing

def rand_ingredients():
    res = []
    for _ in range(randint(1, 10)):
        res.append(rand_ingredient())
    return res

def rand_recipe():
    name = random_string(randint(1, 20))
    prep_time = randint(1, 100)
    cook_time = randint(1, 100)
    serve = randint(1, 10)
    difs = ['hard', 'medium', 'easy']
    dif = choice(difs)
    auts = ['swann', 'Julia', 'guest']
    aut = choice(auts)
    tags = ["Vegetarian",
            "Vegan",
            "Burger",
            "Baby",
            "High protein",
            "Gluten free",
            "Meat",
            "Fish",
            "Cold",
            "Hot",
            "Take away"]
    types = ["Breakfast",
             "Main",
             "Dessert",
             "Fika",
             "Starter",
             "Juice",
             "Smoothie",
             "Soup"]
    type_r = sample(types, randint(1, len(types)))
    tag = sample(tags, randint(1, len(tags)))
    ingredients = rand_ingredients()
    return Recipe(name=name, prep_time=prep_time, cook_time=cook_time, serve=serve, difficulty=dif, author=aut, types=type_r, tags=tag, ingredient_list=ingredients)

def rand_recipes():
    res = []
    for _ in range(randint(5, 10)):
        res.append(rand_recipe())
    return res


book = RecipeBook("my_super_cookbook", "cookbooks/", recipe_list = rand_recipes())
d = book.recipe_list[0].dict
book.edit_recipe(d)
search = {'search_mode': 'recipe_author', 'key': 'swann'}
res = book.find([search])[0]
search_list = [{'search_mode': 'recipe_author', 'key': 'swann'}, {'search_mode': 'ingredient_type', 'key': 'bean'}, {'search_mode': 'recipe_tag', 'key': 'vegan'}, {'search_mode': 'recipe_type', 'key': 'Dessert'}]
r = book.find(search_list)
book.sort_recipes_alphabetically()

rec = Recipe("hoy", 0, 12, 12, 1)

rec.append_ingredient(ing1)

rec.append_ingredient(ings)

rec.remove_ingredient(['apple', ing2])
rec.append_recipe_type(['main', 'breakfast'])
rec.append_recipe_tag(['cold', 'vegan'])
rec.remove_recipe_type(['main'])
rec.remove_recipe_tag(['vegan'])

auto_dict = rec.dict

search_list = [{'search_mode': 'item_name', 'key': 'ap'}, {'search_mode': 'item_type', 'key': 'fruit'}

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