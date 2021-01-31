from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTime
from newIngredientPopup import newIngredientPopup
from editRecipePopup import editRecipePopup
from all_definition import recipe_defs
from recipe import recipe
import food_list as fl
import copy as cp
import recipe
import logging
import copy
from custom_table_items import recipe_table_item
from all_definition import recipe_defs

class myMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.new_ingredient_popup = None
        self.existing_ingredient_popup = None
        self.temp_recipe = None
        #Connect bbuttons
        self.pushButton_select_food_list.clicked.connect(self.pushButton_select_food_list_clicked)
        # connect sorting option in recipe display
        self.tableWidget_recipe.cellDoubleClicked.connect(self.open_edit_recipe_popup)
        self.init_tag_list()
        self.init_meal_type_list()
        self.listWidget_meal_type_list.itemClicked.connect(self.recipe_display_sorting_updated)
        self.listWidget_tag_list.itemClicked.connect(self.recipe_display_sorting_updated)
        self.pushButton_add_new_recipe.clicked.connect(self.new_recipe)
        self.pushButton_delete_recipes.clicked.connect(self.delete_recipes)
        self.checkBox_display_all_meal_type.toggled.connect(self.recipe_display_sorting_updated)
        self.checkBox_display_all_tags.toggled.connect(self.recipe_display_sorting_updated)
        # get the foodlist
        self.foodlist = fl.food_list()
        # load the recipe list
        self.foodlist.set_recipe_db_path('recipe_list_db.json')
        # if the list was imported correctly
        self._import_recipe_list()
        # update the foodlist
        self.table_row_count = 0
        self._init_recipe_table()
#===============================================================================
# Button methods
#================
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


#===============================================================================
# Recipe display
#================
    def recipe_display_sorting_updated(self):
        # make a list of sorting criterias
        criteria_dict = self.get_sorting_criteria_list()
        # get the recipe that match
        recipe_matched = self.get_matching_recipe(criteria_dict)
        # update the display
        # clear the content
        self.tableWidget_recipe.clearContents()
        # resise the table
        for _ in range(self.table_row_count + 1):
            self.tableWidget_recipe.removeRow(self.table_row_count)
            self.table_row_count = self.table_row_count -1
        self.table_row_count = 0
        for rec in recipe_matched:
            self._insert_recipe_line(rec)


    def get_sorting_criteria_list(self):
        sorting_criteria = {'type': [], 'tags': []}
        if not self.checkBox_display_all_meal_type.isChecked():
            for item in self.listWidget_meal_type_list.selectedItems():
                sorting_criteria['type'].append(item.text())
        else:
            sorting_criteria['type'] = recipe_defs().types

        if not self.checkBox_display_all_tags.isChecked():
            for item in self.listWidget_tag_list.selectedItems():
                sorting_criteria['tags'].append(item.text())
        else:
            sorting_criteria['tags'] = recipe_defs().tags
        return sorting_criteria

    def get_matching_recipe(self, criteria_dict):
        recipe_list = []
        for rec in self.foodlist._recipe_list:
            if self.is_recipe_matching_criterias(rec, criteria_dict):
                recipe_list.append(rec)
        return recipe_list

    def is_recipe_matching_criterias(self, recipe, criteria_dict):
        # we do a OR test if one of the criteria match we are done here
        # looking at type first
        for crit in criteria_dict['type']:
            for type in recipe._meta_data['type']:
                if crit == type:
                    for crit_tag in criteria_dict['tags']:
                        for tag in recipe._meta_data['tags']:
                            if crit_tag == tag:
                                return True
                                # we can exit the loop as we are sure a criterion only match one type
        return False


    def _init_recipe_table(self):
        self.tableWidget_recipe.clear()
        self.tableWidget_recipe.setColumnCount(4)
        self.tableWidget_recipe.setHorizontalHeaderLabels(["Name", "Preparation Time", "Type", "Tag"])
        self.tableWidget_recipe.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_recipe.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_recipe.setSortingEnabled(False)
        for rec in self.foodlist._recipe_list:
            self._insert_recipe_line(rec)

    def _insert_recipe_line(self, recipe):
        self.tableWidget_recipe.insertRow(self.table_row_count)
        self.tableWidget_recipe.setItem(self.table_row_count,0, recipe_table_item(recipe))
        self.tableWidget_recipe.setItem(self.table_row_count,1, QTableWidgetItem(str(recipe._meta_data['preptime'] + recipe._meta_data['cooktime'])))
        self.tableWidget_recipe.setItem(self.table_row_count,2, QTableWidgetItem(','.join(recipe._meta_data['type'])))
        self.tableWidget_recipe.setItem(self.table_row_count,3, QTableWidgetItem(','.join(recipe._meta_data['tags'])))
        self.table_row_count = self.table_row_count + 1


    def open_edit_recipe_popup(self, row, col):
        self.editRecipePop = editRecipePopup(self.tableWidget_recipe.item(row,0).recipe)
        self.editRecipePop.updated_recipe.connect(self.update_recipe)

    def new_recipe(self):
        new_recipe = recipe.recipe()
        new_recipe.update_meta_data()
        self.editRecipePop = editRecipePopup(new_recipe)
        self.editRecipePop.updated_recipe.connect(self.add_recipe_to_list)

    def init_tag_list(self):
        for tag in recipe_defs().tags:
            self.listWidget_tag_list.addItem(tag)

    def init_meal_type_list(self):
        for type in recipe_defs().types:
            self.listWidget_meal_type_list.addItem(type)

    def delete_recipes(self):
        selected_recipes = self.tableWidget_recipe.selectedItems()
        if len(selected_recipes) > 0:
            if self.showDialog_delete_recipe():
                for recipe in selected_recipes:
                    if type(recipe) == recipe_table_item:
                        # remove from the recipe list
                        self.foodlist.remove_recipe(recipe.recipe._id)
                        # upadate the saved list
                        self.foodlist.store_recipe_list()
                        # update display
                        self.recipe_display_sorting_updated()
                        # update number of recipes
                        self.update_recipe_number_label()

    def add_recipe_to_list(self, recipe):
        self.foodlist.add_recipe(recipe)
        # save to file
        self.foodlist.store_recipe_list()
        # update the main display
        self.recipe_display_sorting_updated()
        #
        self.update_recipe_number_label()

    def showDialog_delete_recipe(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("Are you sure you want too delete these recipes?")
        msgBox.setWindowTitle("Warning")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        retval = msgBox.exec()
        if retval == QMessageBox.Yes:
            return True
        else:
            return False

#------------------------------------------------------------
# Update_recipe
#------------------------------------------------------------
    def update_recipe(self, recipe):
        #replace the recipe by the updated one
        self.foodlist._recipe_list[recipe._id] = recipe
        # save to file
        self.foodlist.store_recipe_list()
        # update the main display
        self.recipe_display_sorting_updated()

#===============================================================================
# Other methods
#================

    def _import_recipe_list(self):
        import_res = self.foodlist.import_recipe_list()
        if import_res[0]:
            self.label_number_of_recipe.setText(str(self.foodlist.recipe_count))
        else:
            QMessageBox.about(self, "Error", import_res[1])

    def update_recipe_number_label(self):
        self.foodlist._update_recipe_count()
        self.label_number_of_recipe.setText(str(self.foodlist.recipe_count))
