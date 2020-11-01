#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import uic
from PyQt5.QtWidgets import *
import food_list as fl
import ingredient
import copy as cp

# get the food list object
foodlist = fl.food_list()

class newIngredientPopup(QWidget):
    def __init__(self, foodlist):
        # setup the window
        super().__init__()
        uic.loadUi('add_ingredient_popup.ui', self)
        self.pushButton_add_ingredient.clicked.connect(self.add_ingredient_button_clicked)
        self.pushButton_remove_ingredient.clicked.connect(self.pushButton_remove_ingredient_clicked)
        self.pushButton_add_all_to_recipe.clicked.connect(self.pushButton_add_all_to_recipe_clicked)
        #
        self.foodlist = foodlist
        # setup the table
        self.tableWidget_ingredient_list.setColumnCount(5)
        self.row = 0
        self.tableWidget_ingredient_list.insertRow(self.row)
        self.tableWidget_ingredient_list.setItem(self.row,0, QTableWidgetItem("Name"))
        self.tableWidget_ingredient_list.setItem(self.row,1, QTableWidgetItem("Quantity"))
        self.tableWidget_ingredient_list.setItem(self.row,2, QTableWidgetItem("Unit"))
        self.tableWidget_ingredient_list.setItem(self.row,3, QTableWidgetItem("Type"))
        self.tableWidget_ingredient_list.setItem(self.row,4, QTableWidgetItem("Season"))
        self.tableWidget_ingredient_list.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_ingredient_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.show()

    def add_ingredient_button_clicked(self):
        # TO DO check for existing ingredient name, if name already exist, then have a popup to ask if it is ok...
        if not(self.foodlist.check_if_ingredient_exist(self.lineEdit_ingredient_name.text())):
            # add a new row
            self.row = self.row + 1
            self.tableWidget_ingredient_list.insertRow(self.row)
            # add data to table
            self.tableWidget_ingredient_list.setItem(self.row,0, QTableWidgetItem(self.lineEdit_ingredient_name.text()))
            self.tableWidget_ingredient_list.setItem(self.row,1, QTableWidgetItem(str(self.spinBox_quantity.value())))
            self.tableWidget_ingredient_list.setItem(self.row,2, QTableWidgetItem(self.comboBox_unit.currentText()))
            self.tableWidget_ingredient_list.setItem(self.row,3, QTableWidgetItem(self.comboBox_season.currentText()))
            self.tableWidget_ingredient_list.setItem(self.row,4, QTableWidgetItem(self.comboBox_type.currentText()))
        else:
            print("ingredient already present in ingredient list")

    def pushButton_remove_ingredient_clicked(self):
        self.tableWidget_ingredient_list.removeRow(self.row)
        if (self.row > 1):
            self.row = self.row - 1

    def pushButton_add_all_to_recipe_clicked(self):
        # add all to the foodlist
        for index in range(1, self.row+1):
            self.foodlist.add_ingredient(ingredient.ingredient(self.tableWidget_ingredient_list.takeItem(index, 0).text(),
                                                                int(self.tableWidget_ingredient_list.takeItem(index, 1).text()),
                                                                self.tableWidget_ingredient_list.takeItem(index, 2).text(),
                                                                self.tableWidget_ingredient_list.takeItem(index, 3).text(),
                                                                self.tableWidget_ingredient_list.takeItem(index, 4).text()))
        # close the window
        self.close()



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

        # get the foodlist
        self.foodlist = fl.food_list()
        # load the recipe list
        self.foodlist.set_recipe_db_path('recipe_list_db.json')
        self.foodlist.set_ingredient_db_path('ingredient_list_db.json')
        self.foodlist.import_recipe_list()
        self.foodlist.import_ingredient_list()

    def on_add_recipe_button_clicked(self):
        print(self.foodlist.recipe_count)
        print(self.foodlist.ingredient_count)

    # define signal slot interaction here
    def on_add_new_ingredient_button_clicked(self):
        # get a popup
        self.new_ingredient_popup = newIngredientPopup(self.foodlist)
        # add the ingredient to the list

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

    # run the gui
    window.show()
    app.exec()
    # Code goes over here.
    return 0

if __name__ == "__main__":
    main()
