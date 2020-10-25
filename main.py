#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import uic
from PyQt5.QtWidgets import *
import food_list as fl

# get the food list object
foodlist = fl.food_list()

# define signal slot interaction here
def on_add_recipe_button_clicked():
    print(foodlist.recipe_count)

# define signal slot interaction here
def on_add_new_ingredient_button_clicked():
    pass

# define signal slot interaction here
def on_add_existing_ingredient_button_clicked():
    pass

def main():
    """ Main program """

    # load the ui
    app = QApplication([])
    window = QMainWindow()
    uic.loadUi('main_window.ui', window)

    #add recipe button
    pb_add_recipe = window.pushButton_add_recipe
    pb_add_recipe.clicked.connect(on_add_recipe_button_clicked)

    pb_add_new_ingredient = window.pushButton_addnew_ingredient
    pb_add_new_ingredient.clicked.connect(on_add_new_ingredient_button_clicked)

    pb_add_existing_ingredients = window.pushButton_add_existing_ingredients
    pb_add_existing_ingredients.clicked.connect(on_add_existing_ingredient_button_clicked)

    # load the recipe list
    foodlist.set_db_path('recipe_list_db.json')
    foodlist.import_food_list()

    # run the gui
    window.show()
    app.exec()
    # Code goes over here.
    return 0

if __name__ == "__main__":
    main()
