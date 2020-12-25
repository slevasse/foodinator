from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTime
from newIngredientPopup import newIngredientPopup
import food_list as fl
import copy as cp
import recipe
import logging
import copy

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
        # if the list was imported correctly
        self._import_recipe_list()
        self.foodlist.import_ingredient_list()
#===============================================================================
# Button methods
#================
    def start_recipe_button_clicked(self):
        # enable widgets
        self._enable_all_receipe_widgets(True)
        # create a new temporary recipe
        #self.temp_recipe = recipe.recipe()
        self.temp_recipe = recipe.recipe()

#================
    # define signal slot interaction here
    def add_new_ingredient_button_clicked(self):
        # get a popup
        self.new_ingredient_popup = newIngredientPopup(self.temp_recipe._ingredient_list)


#================
    def pushButton_add_recipe_to_list_clicked(self):
        if self._can_I_save_recipe():
            # add receipe fields
            self.temp_recipe.set_name(self.lineEdit_dishname.text())
            # add meta
            self.temp_recipe.update_meta_data(preptime = self.spinBox_preptime.value(),
                                              cooktime = self.spinBox_cooktime.value(),
                                              serve = self.spinBox_serve.value(),
                                              type = self._get_meal_type(),
                                              tags = self._get_tags())
            # add tags
            self.temp_recipe._instruction = self.plainTextEdit_instructions.toPlainText()
            # clear fields
            self._clear_recipe_field()
            # disable fields
            self._enable_all_receipe_widgets(False)
            # add to fooddlist
            self.temp_recipe.print_recipe()
            self.foodlist.add_recipe(self.temp_recipe)
            # clear the temp recipe
            #self.temp_recipe._ingredient_list.clear()
            self.temp_recipe.clear_recipe()
            # update the recipe counter
            self.label_number_of_recipe.setText(str(self.foodlist.recipe_count))
        else:
            QMessageBox.about(self, "Information", "You cannot save a recipe with this few information.")

#================
    def pushButton_select_food_list_clicked(self):
        # ask the user where he wants the folder to be
        filepath = str(QFileDialog.getOpenFileName(self, "Select the new food list location Directory")[0])
        # load the new list
        self.foodlist.set_recipe_db_path(filepath)
        #
        self._import_recipe_list()
        #
        self.label_current_food_list_path.setText(filepath)


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
            self.checkBox_type_breakfast.setEnabled(True)
            self.checkBox_type_main.setEnabled(True)
            self.checkBox_type_dessert.setEnabled(True)
            self.checkBox_type_appetizer.setEnabled(True)
            self.checkBox_type_fika.setEnabled(True)
            self.checkBox_type_smoothie.setEnabled(True)
            self.checkBox_tag_vege.setEnabled(True)
            self.checkBox_tag_vegan.setEnabled(True)
            self.checkBox_tag_baby.setEnabled(True)
            self.checkBox_protein.setEnabled(True)
        else:
            self.pushButton_add_recipe_to_list.setDisabled(True)
            self.lineEdit_dishname.setDisabled(True)
            self.spinBox_preptime.setDisabled(True)
            self.spinBox_cooktime.setDisabled(True)
            self.spinBox_serve.setDisabled(True)
            self.plainTextEdit_instructions.setDisabled(True)
            self.pushButton_addnew_ingredient.setDisabled(True)
            self.checkBox_type_breakfast.setDisabled(True)
            self.checkBox_type_main.setDisabled(True)
            self.checkBox_type_dessert.setDisabled(True)
            self.checkBox_type_appetizer.setDisabled(True)
            self.checkBox_type_fika.setDisabled(True)
            self.checkBox_type_smoothie.setDisabled(True)
            self.checkBox_tag_vege.setDisabled(True)
            self.checkBox_tag_vegan.setDisabled(True)
            self.checkBox_tag_baby.setDisabled(True)
            self.checkBox_protein.setDisabled(True)

    def _import_recipe_list(self):
        import_res = self.foodlist.import_recipe_list()
        if import_res[0]:
            self.label_number_of_recipe.setText(str(self.foodlist.recipe_count))
        else:
            QMessageBox.about(self, "Error", import_res[1])

    def _clear_recipe_field(self):
        self.lineEdit_dishname.clear()
        self.spinBox_preptime.setValue(0)
        self.spinBox_cooktime.setValue(0)
        self.spinBox_serve.setValue(1)
        self.plainTextEdit_instructions.clear()

    def _can_I_save_recipe(self):
        if (self.spinBox_preptime.value() == 0) and (self.spinBox_cooktime.value() == 0):
            return False
        if len(self.lineEdit_dishname.text()) == 0:
            return False
        if len(self.temp_recipe._ingredient_list) == 0:
            return False
        if len(self._get_meal_type()) == 0:
            return False
        # if recipe has no type
        return True

    def _get_meal_type(self):
        type_list = []
        if self.checkBox_type_breakfast.isChecked():
            type_list.append("Breakfast")
        if self.checkBox_type_main.isChecked():
            type_list.append("Main")
        if self.checkBox_type_dessert.isChecked():
            type_list.append("Dessert")
        if self.checkBox_type_appetizer.isChecked():
            type_list.append("Appetizer")
        if self.checkBox_type_fika.isChecked():
            type_list.append("Fika")
        if self.checkBox_type_smoothie.isChecked():
            type_list.append("Smoothie")
        return type_list

    def _get_tags(self):
        tag_list = []
        if self.checkBox_tag_vege.isChecked():
            tag_list.append("Vegetarian")
        if self.checkBox_tag_vegan.isChecked():
            tag_list.append("Vegan")
        if self.checkBox_tag_baby.isChecked():
            tag_list.append("Baby")
        if self.checkBox_protein.isChecked():
            tag_list.append("High_Protein")
        return tag_list
