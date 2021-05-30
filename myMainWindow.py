from PyQt5 import uic
from PyQt5.QtWidgets import *
from foodClasses import *
import logging
import json
from custom_table_items import *
from editRecipePopup import *

class myMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        # class variables
        self.path_app_settings = "app_files/app_setings.json"
        self.cookbook = self._setup_cookbook()
        self.recipe_display_table_row_count = 0
        self.edit_recipe_pop = None
        # setup the UI
        self._setup_recipe_display()
        self._setup_searchbar()
        self._setup_meal_planner()
        self._setup_advanced_search()

#===============================================================================
# setup
#================

    def _setup_recipe_display(self):
        self._init_recipe_table()
        self.pushButton_add_recipe.clicked.connect(self._add_recipe)
        self.pushButton_delete_recipes.clicked.connect(self._del_recipe)
        self.tableWidget_recipe_display.cellDoubleClicked.connect(self.open_edit_recipe_popup)

    def _setup_searchbar(self):
        pass

    def _setup_meal_planner(self):
        pass

    def _setup_advanced_search(self):
        pass

    def _setup_cookbook(self):
        # Manage the input path
        with open(self.path_app_settings, "r") as read_file:
            path = json.load(read_file)['cookbook_path']
        cookbook = RecipeBook()
        # TODO when opening, all settings are copied from the file, if autosave is false, no way to turn it on after...
        cookbook.open(path)
        return cookbook

# ===============================================================================
# Recipe display
# ================
    def _init_recipe_table(self):
        self.tableWidget_recipe_display.clear()
        self.recipe_display_table_row_count = 0
        self.tableWidget_recipe_display.setColumnCount(6)
        self.tableWidget_recipe_display.setHorizontalHeaderLabels(["Name", "Author", "Difficulty", "Preparation Time [minutes]", "Type", "Tag"])
        self.tableWidget_recipe_display.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_recipe_display.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_recipe_display.setSortingEnabled(False)
        for rec in self.cookbook.recipe_list:
            self._insert_recipe_line(rec)

    def _insert_recipe_line(self, recipe: Recipe):
        self.tableWidget_recipe_display.insertRow(self.recipe_display_table_row_count)
        self.tableWidget_recipe_display.setItem(self.recipe_display_table_row_count, 0, RecipeTableItem(recipe))
        self.tableWidget_recipe_display.setItem(self.recipe_display_table_row_count, 1, QTableWidgetItem(recipe.author))
        self.tableWidget_recipe_display.setItem(self.recipe_display_table_row_count, 2, QTableWidgetItem(recipe.difficulty))
        self.tableWidget_recipe_display.setItem(self.recipe_display_table_row_count, 3, QTableWidgetItem(str(recipe.prep_time + recipe.cook_time)))
        self.tableWidget_recipe_display.setItem(self.recipe_display_table_row_count, 4, QTableWidgetItem(','.join(recipe.types)))
        self.tableWidget_recipe_display.setItem(self.recipe_display_table_row_count, 5, QTableWidgetItem(','.join(recipe.tags)))
        self.recipe_display_table_row_count += 1

    def _del_recipe(self):
        selected_recipes = self.tableWidget_recipe_display.selectedItems()
        if len(selected_recipes) > 0:
            if self._showDialog_delete_recipe():
                for recipe in selected_recipes:
                    if type(recipe) == RecipeTableItem:
                        self.cookbook.remove_recipe(recipe.recipe)
        self._refresh_recipe_display()

    def _refresh_recipe_display(self):
        self._init_recipe_table()

    def _showDialog_delete_recipe(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("Are you sure you want too delete this (these) recipe(s)?")
        msg_box.setWindowTitle("Warning")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        retval = msg_box.exec()
        if retval == QMessageBox.Yes:
            return True
        else:
            return False

    def open_edit_recipe_popup(self, row, col):
        self.edit_recipe_pop = EditRecipePopup(self.tableWidget_recipe_display.item(row, 0).recipe)
        self.edit_recipe_pop.updated_recipe.connect(self.update_recipe)

    def update_recipe(self, recipe: Recipe):
        pass

    def _add_recipe(self):
        self.edit_recipe_pop = EditRecipePopup()
        self.edit_recipe_pop.updated_recipe.connect(self.add_recipe_to_list)

    def add_recipe_to_list(self, recipe: Recipe):
        pass
    #         self.foodlist.add_recipe(recipe)
    #         # save to file
    #         self.foodlist.store_recipe_list()
    #         # update the main display
    #         self.recipe_display_sorting_updated()
    #         #
    #         self.update_recipe_number_label()


# #================
#     def pushButton_select_food_list_clicked(self):
#         # ask the user where he wants the folder to be
#         filepath = str(QFileDialog.getOpenFileName(self, "Select the new food list location Directory")[0])
#         # load the new list
#         self.foodlist.set_recipe_db_path(filepath)
#         #
#         self._import_recipe_list()
#         #
#         self.label_current_food_list_path.setText(filepath)
#
#
# #===============================================================================
# # Recipe tab
# #================
#     def recipe_display_sorting_updated(self):
#         # make a list of sorting criterias
#         criteria_dict = self.get_sorting_criteria_list()
#         # get the recipe that match
#         recipe_matched = self.get_matching_recipe(criteria_dict)
#         # update the display
#         # clear the content
#         self.tableWidget_recipe.clearContents()
#         # resise the table
#         for _ in range(self.table_row_count + 1):
#             self.tableWidget_recipe.removeRow(self.table_row_count)
#             self.table_row_count = self.table_row_count -1
#         self.table_row_count = 0
#         for rec in recipe_matched:
#             self._insert_recipe_line(rec)
#
#
#     def get_sorting_criteria_list(self):
#         sorting_criteria = {'type': [], 'tags': []}
#         if not self.checkBox_display_all_meal_type.isChecked():
#             for item in self.listWidget_meal_type_list.selectedItems():
#                 sorting_criteria['type'].append(item.text())
#         else:
#             sorting_criteria['type'] = recipe_defs().types
#
#         if not self.checkBox_display_all_tags.isChecked():
#             for item in self.listWidget_tag_list.selectedItems():
#                 sorting_criteria['tags'].append(item.text())
#         else:
#             sorting_criteria['tags'] = recipe_defs().tags
#         return sorting_criteria
#
#     def get_matching_recipe(self, criteria_dict):
#         recipe_list = []
#         for rec in self.foodlist._recipe_list:
#             if self.is_recipe_matching_criterias(rec, criteria_dict):
#                 recipe_list.append(rec)
#         return recipe_list
#
#     def is_recipe_matching_criterias(self, recipe, criteria_dict):
#         # we do a OR test if one of the criteria match we are done here
#         # looking at type first
#         for crit in criteria_dict['type']:
#             for type in recipe._meta_data['type']:
#                 if crit == type:
#                     for crit_tag in criteria_dict['tags']:
#                         for tag in recipe._meta_data['tags']:
#                             if crit_tag == tag:
#                                 return True
#                                 # we can exit the loop as we are sure a criterion only match one type
#         return False
#
#
#
#
#
#
#     def add_recipe_to_list(self, recipe):
#         self.foodlist.add_recipe(recipe)
#         # save to file
#         self.foodlist.store_recipe_list()
#         # update the main display
#         self.recipe_display_sorting_updated()
#         #
#         self.update_recipe_number_label()
#
#     def showDialog_delete_recipe(self):
#         msgBox = QMessageBox()
#         msgBox.setIcon(QMessageBox.Warning)
#         msgBox.setText("Are you sure you want too delete these recipes?")
#         msgBox.setWindowTitle("Warning")
#         msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
#         retval = msgBox.exec()
#         if retval == QMessageBox.Yes:
#             return True
#         else:
#             return False
#
# #------------------------------------------------------------
# # Update_recipe
# #------------------------------------------------------------

#
# #===============================================================================
# # Recipe list generator related
# #===============================================================================
#
#     def init_recipe_generator(self):
#         #add the generator object
#         self.recipe_list_generator = recipe_list_generator()
#         # selected food list table
#         self.tableWidget_search_configurations.clear()
#         self.tableWidget_search_configurations.setColumnCount(5)
#         self.tableWidget_search_configurations.setHorizontalHeaderLabels(["How many people", "How many days","Lunch and dinner", "Meal type(s)", "with tag(s)"])
#         self.tableWidget_search_configurations.horizontalHeader().setStretchLastSection(True)
#         self.tableWidget_search_configurations.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
#         self.tableWidget_search_configurations.setSortingEnabled(False)
#
#         # tag list
#         self.init_search_tag_list()
#         # type list
#         self.init_search_meal_type_list()
#         # search ressult table
#         self.tableWidget_search_results.clear()
#         self.tableWidget_search_results.setColumnCount(2)
#         self.tableWidget_search_results.setHorizontalHeaderLabels(["Name", "Meal type"])
#         self.tableWidget_search_results.horizontalHeader().setStretchLastSection(True)
#         self.tableWidget_search_results.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
#         self.tableWidget_search_results.setSortingEnabled(False)
#
#
#     def init_search_tag_list(self):
#         for tag in recipe_defs().tags:
#             self.listWidget_search_meal_tags.addItem(tag)
#
#     def init_search_meal_type_list(self):
#         for type in recipe_defs().types:
#             self.listWidget_search_meal_type.addItem(type)
#
#     def connect_all(self):
#         self.pushButton_add_search_configuration.clicked.connect(self.add_new_search_configuration)
#         self.pushButton_delete_selected_configurations.clicked.connect(self.delete_selected_search_configuration)
#         self.pushButton_make_food_list.clicked.connect(self.make_food_list)
#
#     def add_new_search_configuration(self):
#         # get types and and tags
#         types = []
#         tags = []
#         for item in self.listWidget_search_meal_type.selectedItems():
#             types.append(item.text())
#         for item in self.listWidget_search_meal_tags.selectedItems():
#             tags.append(item.text())
#         config = search_configuration_def(self.spinBox_search_how_many_people.value(),
#                                           self.spinBox_how_many_days.value(),
#                                           self.checkBox_main_count_as_lunch_and_dinner.isChecked(),
#                                           types,
#                                           tags)
#
#         self.insert_search_configuration_line(config)
#
#     def insert_search_configuration_line(self, configuration):
#         self.tableWidget_search_configurations.insertRow(self.search_configuration_table_row_count)
#         self.tableWidget_search_configurations.setItem(self.search_configuration_table_row_count,0, search_configuration_table_item(configuration))
#         self.tableWidget_search_configurations.setItem(self.search_configuration_table_row_count,1, QTableWidgetItem(str(self.spinBox_how_many_days.value())))
#         self.tableWidget_search_configurations.setItem(self.search_configuration_table_row_count,2, QTableWidgetItem(str(self.checkBox_main_count_as_lunch_and_dinner.isChecked())))
#         self.tableWidget_search_configurations.setItem(self.search_configuration_table_row_count,3, QTableWidgetItem(','.join(configuration.configuration['type'])))
#         self.tableWidget_search_configurations.setItem(self.search_configuration_table_row_count,4, QTableWidgetItem(','.join(configuration.configuration['tags'])))
#         self.search_configuration_table_row_count = self.search_configuration_table_row_count + 1
#
#     def delete_selected_search_configuration(self):
#         selected_configs = self.tableWidget_search_configurations.selectedItems()
#         for conf in selected_configs:
#             self.tableWidget_search_configurations.removeRow(self.tableWidget_search_configurations.row(conf))
#             self.search_configuration_table_row_count = self.search_configuration_table_row_count - 1
#
#
#     def make_food_list(self):
#         # for each search search configuration
#         for row in range(self.tableWidget_search_configurations.rowCount()):
#             # get the configuration from the table
#             config = self.tableWidget_search_configurations.item(row, 0).configuration.configuration
#             # find how many recipe we have to select
#             search_result = self.get_matching_random_recipe(config, config["day count"])
#             # display
#             self.add_new_search_result(search_result)
#
#     def get_matching_random_recipe(self, search_config, N):
#         crit_dict = {'type': search_config["type"], 'tags': search_config["tags"]}
#         recipe_list = []
#         count = 0
#         foodlist_rand = sample(self.foodlist._recipe_list, len(self.foodlist._recipe_list))
#         for rec in foodlist_rand:
#             if count < N:
#                 if self.is_recipe_matching_criterias(rec, crit_dict):
#                     recipe_list.append(rec)
#                     count += 1
#             else:
#                 break
#         return recipe_list
#         # get a randomised food list
#
#     def add_new_search_result(self, recipe_list):
#         for recipe in recipe_list:
#             self.insert_search_result_line(recipe)
#
#     def insert_search_result_line(self, recipe):
#         self.tableWidget_search_results.insertRow(self.search_results_table_row_count)
#         self.tableWidget_search_results.setItem(self.search_results_table_row_count,0, recipe_table_item(recipe))
#         self.tableWidget_search_results.setItem(self.search_results_table_row_count,1, QTableWidgetItem(','.join(recipe._meta_data['type'])))
#         self.search_results_table_row_count = self.search_results_table_row_count + 1
#
#     def delete_selected_search_result(self):
#         selected_configs = self.tableWidget_search_results.selectedItems()
#         for conf in selected_configs:
#             self.tableWidget_search_results.removeRow(self.tableWidget_search_results.row(conf))
#             self.search_results_table_row_count = self.search_results_table_row_count - 1
#
# #===============================================================================
# # Other methods
# #================
#
#     def _import_recipe_list(self):
#         import_res = self.foodlist.import_recipe_list()
#         if import_res[0]:
#             self.label_number_of_recipe.display(self.foodlist.recipe_count)
#         else:
#             QMessageBox.about(self, "Error", import_res[1])
#
#     def update_recipe_number_label(self):
#         self.foodlist._update_recipe_count()
#         self.label_number_of_recipe.display(self.foodlist.recipe_count)
