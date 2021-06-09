from PyQt5 import uic
from PyQt5.QtWidgets import *
from foodClasses import *
import logging
import json
from custom_table_items import *
from editRecipePopup import *
import re

class myMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        # class variables
        self.path_app_settings = "app_files/app_setings.json"
        self.cookbook = self._setup_cookbook()
        self.recipe_display_table_row_count = 0
        self.edit_recipe_pop = None
        self.filtered_recipes = None
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
        # name
        self.lineEdit_recipe_name_seach.textChanged.connect(self.search_recipes)
        self.listWidget_recipe_name_search.itemDoubleClicked.connect(self.add_to_selected_recipe_name_list)
        self.listWidget_recipe_name_selection.itemDoubleClicked.connect(self.del_from_selected_recipe_name_list)
        # author
        self.lineEdit_recipe_author_name_search.textChanged.connect(self.search_recipes)
        self.listWidget_recipe_author_search.itemDoubleClicked.connect(self.add_to_selected_recipe_author_list)
        self.listWidget_recipe_author_selection.itemDoubleClicked.connect(self.del_from_selected_recipe_author_list)
        # difficulty
        self.lineEdit_recipe_dificulty_search.textChanged.connect(self.search_recipes)
        self.listWidget_recipe_difficulty_search.itemDoubleClicked.connect(self.add_to_selected_recipe_difficulty_list)
        self.listWidget_recipe_difficulty_selection.itemDoubleClicked.connect(self.del_from_selected_recipe_difficulty_list)
        # tag
        self.lineEdit_recipe_tag_search.textChanged.connect(self.search_recipes)
        self.listWidget_recipe_tag_search.itemDoubleClicked.connect(self.add_to_selected_recipe_tag_list)
        self.listWidget_recipe_tag_selection.itemDoubleClicked.connect(self.del_from_selected_recipe_tag_list)
        # type
        self.lineEdit_recipe_type_search.textChanged.connect(self.search_recipes)
        self.listWidget_recipe_type_search.itemDoubleClicked.connect(self.add_to_selected_recipe_type_list)
        self.listWidget_recipe_type_selection.itemDoubleClicked.connect(self.del_from_selected_recipe_type_list)
        # ingredient name
        self.lineEdit_ingredient_name_search.textChanged.connect(self.search_recipes)
        self.listWidget_ingredient_name_search.itemDoubleClicked.connect(self.add_to_selected_recipe_ingredient_name_list)
        self.listWidget_recipe_ingredient_name_selection.itemDoubleClicked.connect(self.del_from_selected_recipe_ingredient_name_list)
        # ingredient type
        self.lineEdit_ingredient_type_search.textChanged.connect(self.search_recipes)
        self.listWidget_ingredient_type_search.itemDoubleClicked.connect(self.add_to_selected_recipe_ingredient_type_list)
        self.listWidget_recipe_ingredient_type_selection.itemDoubleClicked.connect(self.del_from_selected_recipe_ingredient_type_list)
        # ingredient season
        self.lineEdit_ingredient_season_search.textChanged.connect(self.search_recipes)
        self.search_recipes()

    def _setup_meal_planner(self):
        pass

    def _setup_advanced_search(self):
        pass

    def _setup_cookbook(self):
        # TODO include a case for when the file is missing.
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
        # clear the table
        self.tableWidget_recipe_display.clear()
        self.recipe_display_table_row_count = 0
        self.tableWidget_recipe_display.setColumnCount(6)
        self.tableWidget_recipe_display.setHorizontalHeaderLabels(["Name", "Author", "Difficulty", "Preparation Time [minutes]", "Type", "Tag"])
        self.tableWidget_recipe_display.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_recipe_display.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_recipe_display.setSortingEnabled(False)
        if self.filtered_recipes is None:
            for rec in self.cookbook.recipe_list:
                self._insert_recipe_line(rec)
            self.tableWidget_recipe_display.setRowCount(len(self.cookbook.recipe_list))
        else:
            for rec in self.filtered_recipes:
                self._insert_recipe_line(rec)
            self.tableWidget_recipe_display.setRowCount(len(self.filtered_recipes))

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
                        self.tableWidget_recipe_display.removeRow(self.tableWidget_recipe_display.row(recipe))
                        self.recipe_display_table_row_count -= 1

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

# ===============================================================================
# Add or edit a recipe
# ================

    def open_edit_recipe_popup(self, row, col):
        self.edit_recipe_pop = EditRecipePopup(self.tableWidget_recipe_display.item(row, 0).recipe)
        self.edit_recipe_pop.updated_recipe.connect(self.edit_recipe)

    def edit_recipe(self, recipe_dict: dict):
        self.edit_recipe_pop = None
        self.cookbook.sort_recipes_alphabetically()
        self.cookbook._auto_save()
        self._refresh_recipe_display()

    def _add_recipe(self):
        self.edit_recipe_pop = EditRecipePopup()
        self.edit_recipe_pop.updated_recipe.connect(self.add_recipe_to_list)

    def add_recipe_to_list(self, recipe_dict: dict):
        self.edit_recipe_pop = None
        self.cookbook.append(recipe_dict)
        self._refresh_recipe_display()

# ===============================================================================
# Recipe sorting
# ================
# add and del items from the lists
    def add_to_selected_recipe_name_list(self):
        self.generic_add_to_selected_recipe_parameter_list(self.listWidget_recipe_name_search,
                                                           self.listWidget_recipe_name_selection)

    def del_from_selected_recipe_name_list(self):
        self.generic_del_from_selected_recipe_parameter_list(self.listWidget_recipe_name_selection)

    def add_to_selected_recipe_author_list(self):
        self.generic_add_to_selected_recipe_parameter_list(self.listWidget_recipe_author_search,
                                                           self.listWidget_recipe_author_selection)

    def del_from_selected_recipe_author_list(self):
        self.generic_del_from_selected_recipe_parameter_list(self.listWidget_recipe_author_selection)

    def add_to_selected_recipe_difficulty_list(self):
        self.generic_add_to_selected_recipe_parameter_list(self.listWidget_recipe_difficulty_search,
                                                           self.listWidget_recipe_difficulty_selection)

    def del_from_selected_recipe_difficulty_list(self):
        self.generic_del_from_selected_recipe_parameter_list(self.listWidget_recipe_difficulty_selection)

    def add_to_selected_recipe_tag_list(self):
        self.generic_add_to_selected_recipe_parameter_list(self.listWidget_recipe_tag_search,
                                                           self.listWidget_recipe_tag_selection)

    def del_from_selected_recipe_tag_list(self):
        self.generic_del_from_selected_recipe_parameter_list(self.listWidget_recipe_tag_selection)

    def add_to_selected_recipe_type_list(self):
        self.generic_add_to_selected_recipe_parameter_list(self.listWidget_recipe_type_search,
                                                           self.listWidget_recipe_type_selection)

    def del_from_selected_recipe_type_list(self):
        self.generic_del_from_selected_recipe_parameter_list(self.listWidget_recipe_type_selection)

    def add_to_selected_recipe_ingredient_name_list(self):
        self.generic_add_to_selected_recipe_parameter_list(self.listWidget_ingredient_name_search,
                                                           self.listWidget_recipe_ingredient_name_selection)

    def del_from_selected_recipe_ingredient_name_list(self):
        self.generic_del_from_selected_recipe_parameter_list(self.listWidget_recipe_ingredient_name_selection)

    def add_to_selected_recipe_ingredient_type_list(self):
        self.generic_add_to_selected_recipe_parameter_list(self.listWidget_ingredient_type_search,
                                                           self.listWidget_recipe_ingredient_type_selection)

    def del_from_selected_recipe_ingredient_type_list(self):
        self.generic_del_from_selected_recipe_parameter_list(self.listWidget_recipe_ingredient_type_selection)

    def generic_add_to_selected_recipe_parameter_list(self, display_list: QListWidget, selected_list: QListWidget):
        for item in display_list.selectedItems():
            test = True
            for index in range(selected_list.count()):
                if item.text() == selected_list.item(index).text():
                    test = False
            if test:
                selected_list.addItem(item.text())
        self.search_recipes()

    def generic_del_from_selected_recipe_parameter_list(self, selected_list: QListWidget):
        for item in selected_list.selectedItems():
            selected_list.takeItem(selected_list.row(item))
        self.search_recipes()

# search core
    def search_recipes(self):
        self.update_search_filter()
        self.update_search_form_display()
        self._init_recipe_table()

    def update_search_form_display(self):
        self.clear_all_filter_list()
        unique_atributes = self.cookbook.find_unique_attributes(self.filtered_recipes)
        # name
        self.generic_update_search_list(unique_atributes[0],
                                        self.lineEdit_recipe_name_seach,
                                        self.listWidget_recipe_name_search)
        # author
        self.generic_update_search_list(unique_atributes[1],
                                        self.lineEdit_recipe_author_name_search,
                                        self.listWidget_recipe_author_search)
        # difficulty
        self.generic_update_search_list(unique_atributes[2],
                                        self.lineEdit_recipe_dificulty_search,
                                        self.listWidget_recipe_difficulty_search)
        # tag
        self.generic_update_search_list(unique_atributes[3],
                                        self.lineEdit_recipe_tag_search,
                                        self.listWidget_recipe_tag_search)
        # type
        self.generic_update_search_list(unique_atributes[4],
                                        self.lineEdit_recipe_type_search,
                                        self.listWidget_recipe_type_search)
        # ingredient name
        self.generic_update_search_list(unique_atributes[5],
                                        self.lineEdit_ingredient_name_search,
                                        self.listWidget_ingredient_name_search)
        # ingredient type
        self.generic_update_search_list(unique_atributes[6],
                                        self.lineEdit_ingredient_type_search,
                                        self.listWidget_ingredient_type_search)
        # ingredient season
        self.generic_update_search_list(unique_atributes[7],
                                        self.lineEdit_ingredient_season_search,
                                        self.listWidget_ingredient_season_search)

    def generic_update_search_list(self, unique_identifiers: list, line_edit: QLineEdit, display_list: QListWidget):
        key_list = list(unique_identifiers)
        key_list.sort()
        if len(line_edit.text().lstrip().rstrip()) > 0:
            for key in key_list:
                if re.search(line_edit.text().lstrip().rstrip(), key, re.IGNORECASE):
                    display_list.addItem(key)
        else:
            display_list.addItems(key_list)

    def clear_all_filter_list(self):
        self.listWidget_recipe_name_search.clear()
        self.listWidget_recipe_author_search.clear()
        self.listWidget_recipe_difficulty_search.clear()
        self.listWidget_recipe_tag_search.clear()
        self.listWidget_recipe_type_search.clear()
        self.listWidget_ingredient_name_search.clear()
        self.listWidget_ingredient_type_search.clear()
        self.listWidget_ingredient_season_search.clear()

    def update_search_filter(self):
        search_filter = []
        search_filter += self.generic_get_filter("recipe_name",
                                                 self.lineEdit_recipe_name_seach,
                                                 self.listWidget_recipe_name_selection)

        search_filter += self.generic_get_filter("recipe_author",
                                                 self.lineEdit_recipe_author_name_search,
                                                 self.listWidget_recipe_author_selection)

        search_filter += self.generic_get_filter("recipe_tag",
                                                 self.lineEdit_recipe_tag_search,
                                                 self.listWidget_recipe_tag_selection)

        search_filter += self.generic_get_filter("recipe_type",
                                                 self.lineEdit_recipe_type_search,
                                                 self.listWidget_recipe_type_selection)

        search_filter += self.generic_get_filter("recipe_difficulty",
                                                 self.lineEdit_recipe_dificulty_search,
                                                 self.listWidget_recipe_difficulty_selection)

        search_filter += self.generic_get_filter("ingredient_name",
                                                 self.lineEdit_ingredient_name_search,
                                                 self.listWidget_recipe_ingredient_name_selection)

        search_filter += self.generic_get_filter("ingredient_type",
                                                 self.lineEdit_ingredient_type_search,
                                                 self.listWidget_recipe_ingredient_type_selection)

        search_filter += self.generic_get_filter("ingredient_season",
                                                 self.lineEdit_ingredient_season_search,
                                                 self.listWidget_recipe_ingredient_season_selection)

        print(search_filter)
        if len(search_filter) == 0:
            self.filtered_recipes = self.cookbook.recipe_list
        else:
            self.filtered_recipes = self.cookbook.find(search_filter)

    def generic_get_filter(self, search_mode: str, line_edit: QLineEdit, list_widget: QListWidget):
        selected = list_widget.selectedItems()
        text = line_edit.text().lstrip().rstrip()
        search_from_list = []
        # use the line edit
        if len(text) > 0:
            search_from_list.append({'search_mode': search_mode, 'key': text})
        for index in range(list_widget.count()):
            search_from_list.append({'search_mode': search_mode, 'key': list_widget.item(index).text()})
        return search_from_list

# #================
