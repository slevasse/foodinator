#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import uic
from PyQt5.QtWidgets import *
import food_list as fl

# get the food list object
foodlist = fl.food_list()

class myMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.new_ingredient_popup = None
        self.existing_ingredient_popup = None
        #add recipe button
        self.pb_add_recipe = self.pushButton_add_recipe
        self.pb_add_recipe.clicked.connect(self.on_add_recipe_button_clicked)

        self.pb_add_new_ingredient = self.pushButton_addnew_ingredient
        self.pb_add_new_ingredient.clicked.connect(self.on_add_new_ingredient_button_clicked)

        self.pb_add_existing_ingredients = self.pushButton_add_existing_ingredients
        self.pb_add_existing_ingredients.clicked.connect(self.on_add_existing_ingredient_button_clicked)

    def on_add_recipe_button_clicked(self):
        print(foodlist.recipe_count)

    # define signal slot interaction here
    def on_add_new_ingredient_button_clicked(self):
        # get a popup
        self.new_ingredient_popup = QWidget()
        uic.loadUi('add_ingredient_popup.ui', self.new_ingredient_popup)
        self.new_ingredient_popup.show()

    # define signal slot interaction here
    def on_add_existing_ingredient_button_clicked(self):
        # get a popup
        self.existing_ingredient_popup = QWidget()
        uic.loadUi('add_existing_ingredient.ui', self.existing_ingredient_popup)
        self.existing_ingredient_popup.show()


def main():
    """ Main program """

    # load the ui
    app = QApplication([])
    #window = QMainWindow()
    window = myMainWindow()

    # load the recipe list
    foodlist.set_recipe_db_path('recipe_list_db.json')
    foodlist.set_ingredient_db_path('ingredient_list_db.json')
    foodlist.import_recipe_list()
    foodlist.import_ingredient_list()

    # run the gui
    window.show()
    app.exec()
    # Code goes over here.
    return 0

if __name__ == "__main__":
    main()
