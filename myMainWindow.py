from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTime
from newIngredientPopup import newIngredientPopup
import food_list as fl
import copy as cp
import recipe
import logging

class myMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.new_ingredient_popup = None
        self.existing_ingredient_popup = None
        self.temp_recipe = None
        #Connect bbuttons
        self.pushButton_start_new_receipe.clicked.connect(self.start_recipe_button_clicked)
        self.pushButton_addnew_ingredient.clicked.connect(self.add_new_ingredient_button_clicked)
        #self.pushButton_add_existing_ingredients.clicked.connect(self.add_existing_ingredient_button_clicked)
        self.pushButton_add_recipe_to_list.clicked.connect(self.pushButton_add_recipe_to_list_clicked)
        self.pushButton_select_food_list.clicked.connect(self.pushButton_select_food_list_clicked)
        self.pushButton_select_ingredient_list.clicked.connect(self.pushButton_select_ingredient_list_clicked)

        # get the foodlist
        self.foodlist = fl.food_list()
        # load the recipe list
        self.foodlist.set_recipe_db_path('recipe_list_db.json')
        self.foodlist.set_ingredient_db_path('ingredient_list_db.json')
        self.foodlist.import_recipe_list()
        self.foodlist.import_ingredient_list()
#===============================================================================
# Button methods
#================
    def start_recipe_button_clicked(self):
        # enable widgets
        self._enable_all_receipe_widgets(True)
        # create a new temporary recipe
        self.temp_recipe = recipe.recipe()

#================
    # define signal slot interaction here
    def add_new_ingredient_button_clicked(self):
        # get a popup
        self.new_ingredient_popup = newIngredientPopup(self.temp_recipe)


#================
    # define signal slot interaction here
    def add_existing_ingredient_button_clicked(self):
        # get a popup
        self.existing_ingredient_popup = QWidget()
        uic.loadUi('add_existing_ingredient.ui', self.existing_ingredient_popup)
        self.existing_ingredient_popup.show()

#================
    def pushButton_add_recipe_to_list_clicked(self):
        # add receipe fields
        self.temp_recipe.set_name(self.lineEdit_dishname.text())
        # add meta
        self.temp_recipe.update_meta_data(preptime = self.spinBox_preptime.value(), cooktime = self.spinBox_cooktime.value(), serve = self.spinBox_serve.value())
        # add tags
        self.temp_recipe._instruction = self.plainTextEdit_instructions.toPlainText()
        # clear fields
        self._clear_recipe_field()
        # disable fields
        self._enable_all_receipe_widgets(False)
        # add to fooddlist
        self.foodlist.add_recipe(self.temp_recipe)
        # clear the temp recipe
        self.temp_recipe = None
        # update the recipe count view
        self.foodlist._recipe_list[-1].print_recipe()


#================
    def pushButton_select_food_list_clicked(self):
        # ask the user where he wants the folder to be
        filepath = str(QFileDialog.getOpenFileName(self, "Select the new food list location Directory")[0])
        # check if the path is a valid file
        if self.foodlist.check_if_list_path_is_correct(filepath):
            # load the new list
            self.foodlist.set_recipe_db_path(filepath)
            #
            self.foodlist.import_recipe_list()
            #
            self.label_current_food_list_path.setText(filepath)
        else:
            QMessageBox.about(self, "Error", "The file selected is not a valid recipe-list. Please retry.")



    def pushButton_select_ingredient_list_clicked(self):
        filepath = str(QFileDialog.getOpenFileName(self, "Select the new ingredient list location Directory")[0])
        # load the new list
        if self.foodlist.check_if_list_path_is_correct(filepath):
            # load the new list
            self.foodlist.set_ingredient_db_path(filepath)
            #
            self.foodlist.import_ingredient_list()
            #
            self.label_ingredient_list_path.setText(filepath)
        else:
            QMessageBox.about(self, "Error", "The file selected is not a valid ingredient-list. Please retry.")


#===============================================================================
# Other methods
#================
    def _enable_all_receipe_widgets(self, enable):
        if (enable):
            self.pushButton_add_recipe_to_list.setEnabled(True)
            self.lineEdit_dishname.setEnabled(True)
            self.spinBox_preptime.setEnabled(True)
            self.spinBox_cooktime.setEnabled(True)
            self.spinBox_serve.setEnabled(True)
            self.plainTextEdit_instructions.setEnabled(True)
            self.pushButton_addnew_ingredient.setEnabled(True)
        else:
            self.pushButton_add_recipe_to_list.setDisabled(True)
            self.lineEdit_dishname.setDisabled(True)
            self.spinBox_preptime.setDisabled(True)
            self.spinBox_cooktime.setDisabled(True)
            self.spinBox_serve.setDisabled(True)
            self.plainTextEdit_instructions.setDisabled(True)
            self.pushButton_addnew_ingredient.setDisabled(True)


    def _clear_recipe_field(self):
        self.lineEdit_dishname.clear()
        self.spinBox_preptime.setValue(0)
        self.spinBox_cooktime.setValue(0)
        self.spinBox_serve.setValue(1)
        self.plainTextEdit_instructions.clear()
