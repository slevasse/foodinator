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
    id = randint(1, 3000)
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

    return Recipe(name, id, prep_time, cook_time, serve, dif, aut, type_r, tag, ingredients)

def rand_recipes():
    res = []
    for _ in range(randint(500, 1000)):
        res.append(rand_recipe())
    return res


get_name = lambda recipe: recipe.name

book = RecipeBook("my_super_cookbook", "cookbooks/", recipe_list = rand_recipes())

search = {'search_mode': 'recipe_author', 'key': 'swann'}
search_list = [{'search_mode': 'recipe_author', 'key': 'swann'}, {'search_mode': 'ingredient_type', 'key': 'bean'}, {'search_mode': 'recipe_tag', 'key': 'vegan'}, {'search_mode': 'recipe_type', 'key': 'Dessert'}]
r = book.find(search_list)

hel = book.find_matching_name('hel')
kiwi = book.find_with_ingredient_name('kiwi')
crozet = book.find_with_ingredient_name('crozet')
dif = book.find_with_difficulty('hard')
aut = book.find_with_author('swann')
types = book.find_with_ingredient_type('soy')
tag = book.find_with_tag('baby')
typ = book.find_with_type('soup')
seas = book.find_with_ingredient_season('all')

detailed = book.find_with_tag('baby', book.find_with_author('julia'))

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