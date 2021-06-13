from PyQt5 import uic
from PyQt5.QtWidgets import *
from foodClasses import *
import logging
from AppDefaults import AppDefaults
import json
from custom_table_items import *
from editRecipePopup import *
from random import *
import re

class myMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        # class variables
        self.path_app_settings = AppDefaults().application_settings_path
        self.cookbook_path = None
        self.cookbook_backup_folder_path = None
        self.food_library_path = None
        self.cookbook = None
        self.edit_recipe_pop = None
        self.filtered_recipes = None
        self.search_filter = None
        self.aggregated_ingredient_list = []
        self._setup_application()
        # setup the UI
        self._setup_recipe_display()
        self._setup_searchbar()
        self._setup_meal_planner()
        self._setup_advanced_search()
        self.new_cookbook_popup = None

#===============================================================================
# setup
#================

    def _setup_recipe_display(self):
        self._init_recipe_table()
        self.update_recipe_table()
        self.pushButton_add_recipe.clicked.connect(self._add_recipe)
        self.pushButton_delete_recipes.clicked.connect(self._del_recipe)
        self.tableWidget_recipe_display.cellDoubleClicked.connect(self.open_edit_recipe_popup)

    def _setup_searchbar(self):
        # duration
        self.horizontalSlider_prep_time_filter.valueChanged.connect(self.search_recipes)
        self.horizontalSlider_prep_time_filter.setMaximum(self.cookbook.longest)
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
        self._init_meal_planner()
        self.pushButton_delete_selected_search_result.clicked.connect(self.delete_selected_search_results)
        self.pushButton_add_selection_to_meal_planner.clicked.connect(self.add_manual_search_result)
        self.pushButton_add_parametric_selection_to_mael_planner.clicked.connect(self.add_parametric_search_result)
        self.pushButton_re_suffle_parametric_selection.clicked.connect(self.re_shuffle_parametric_item)
        self.tableWidget_meal_planner_recipes.itemSelectionChanged.connect(self.update_planer_info_view)
        self.pushButton_add_new_from_selection.clicked.connect(self.add_new_recipe_from_selection)

    def _setup_advanced_search(self):
        pass

    def _setup_application(self):
        # logger
        logging.basicConfig(filename=AppDefaults().logging_path, format=AppDefaults().logging_format, level=logging.INFO)  # use INFO in release
        logging.info('App Started.')
        # read parameter from setting file.
        self._load_application_settings()
        # application menubar
        self.actionOpen.triggered.connect(self.action_open)
        self.actionNew_cookook.triggered.connect(self.action_new)

# ===============================================================================
# Application settings and management
# ================

    def _load_application_settings(self):
        # read parameter from setting file.
        # If we fail, notify the user and create a new one.
        try:
            with open(self.path_app_settings, "r") as read_file:
                settings = json.load(read_file)
                self.cookbook_path = settings["cookbook_path"]
                self.cookbook_backup_folder_path = settings["cookbook_backup_folder_path"]
                self._open_cookbook(self.cookbook_path)
        except (OSError, IOError) as err:
            logging.warning("In _load_application_settings, {0}".format(err))
            # TODO
            logging.warning("In _load_application_settings, create a new application setting file at :" + AppDefaults().application_settings_path)
            self._showDialog_user_info("The setting file required to start the program was not found. Starting with default settings",
                                       "Application settings not found!")
            # default settings
            self._set_cookbook_to_default()

    def _open_cookbook(self, path: str):
        self.cookbook = RecipeBook()
        try:
            self.cookbook.open(path)
        except TypeError as err:
            logging.error("In '_open_cookbook', TypeError: {0}".format(err))
            self._showDialog_user_info(
                "The file provided does not have the right file extension. Please try again.",
                "Cookbook file extension is wrong!")
            self._set_cookbook_to_default()
        except (OSError, IOError) as err:
            logging.error("In '_open_cookbook', {0}".format(err))
            self._showDialog_user_info("Cookbook file not found. If it is the first time you open this program, ignore this message.", "Cookbook file not found!")
            self._set_cookbook_to_default()

    def _set_cookbook_to_default(self):
        self.cookbook = RecipeBook(AppDefaults().default_cookbook_name,
                                   AppDefaults().default_cookbook_path,
                                   auto_save=AppDefaults().default_cookbook_autosave_state,
                                   auto_backup=AppDefaults().default_cookbook_autosave_state,
                                   backup_interval=AppDefaults().default_cookbook_backup_interval,
                                   backup_history_length=AppDefaults().default_cookbook_backup_history_length)

    def _write_application_settings(self):
        # TODO
        pass

    def _showDialog_user_info(self, message: str, title: str):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

    def action_open(self):
        filename = QFileDialog.getOpenFileName(self, 'Open cookbook file', '', "Cookbook file (*" + Definitions().cookbook_file_extention + ")")[0]
        self._open_cookbook(filename)

    def action_new(self):
        self.new_cookbook_popup = None
        self.new_cookbook_popup = QWidget()
        uic.loadUi('new_cookbook_popup.ui', self.new_cookbook_popup)
        self.new_cookbook_popup.spinBox_backup_history.setValue(AppDefaults().default_cookbook_backup_history_length)
        self.new_cookbook_popup.spinBox_backup_interval.setValue(AppDefaults().default_cookbook_backup_interval)
        self.new_cookbook_popup.checkBox_autosave.setChecked(AppDefaults().default_cookbook_autosave_state)
        self.new_cookbook_popup.checkBox_backup.setChecked(AppDefaults().default_cookbook_autosave_state)
        self.new_cookbook_popup.pushButton_ok.clicked.connect(self.action_New_ok)
        self.new_cookbook_popup.pushButton_cancel.clicked.connect(self.action_New_cancel)
        self.new_cookbook_popup.pushButton_location.clicked.connect(self.action_New_filelocation)
        self.new_cookbook_popup.show()

    def action_New_ok(self):
        self.new_cookbook_popup.close()
        self.new_cookbook_popup = None
        pass

    def action_New_filelocation(self):


    def action_New_cancel(self):
        self.new_cookbook_popup.close()
        self.new_cookbook_popup = None

# ===============================================================================
# Recipe display
# ================
    def _init_recipe_table(self):
        self.tableWidget_recipe_display.setColumnCount(7)
        self.tableWidget_recipe_display.setHorizontalHeaderLabels(["Name", "Author", "Difficulty", "Prep Time", "Servings", "Type", "Tag"])
        self.tableWidget_recipe_display.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_recipe_display.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)#QHeaderView.Stretch)
        self.tableWidget_recipe_display.setSortingEnabled(False)
        self.tableWidget_recipe_display.setWordWrap(True)

    def update_recipe_table(self):
        # remove all rows
        self.tableWidget_recipe_display.setRowCount(0)
        # add new rows
        if self.filtered_recipes is None:
            for rec in self.cookbook.recipe_list:
                self._insert_recipe_line(rec)
            self.tableWidget_recipe_display.setRowCount(len(self.cookbook.recipe_list))
        else:
            for rec in self.filtered_recipes:
                self._insert_recipe_line(rec)
            self.tableWidget_recipe_display.setRowCount(len(self.filtered_recipes))
        # resize table
        self.tableWidget_recipe_display.resizeRowsToContents()

    def _insert_recipe_line(self, recipe: Recipe):
        self.tableWidget_recipe_display.insertRow(self.tableWidget_recipe_display.rowCount())
        self.tableWidget_recipe_display.setItem(self.tableWidget_recipe_display.rowCount() - 1, 0, RecipeTableItem(recipe))
        self.tableWidget_recipe_display.setItem(self.tableWidget_recipe_display.rowCount() - 1, 1, QTableWidgetItem(recipe.author))
        self.tableWidget_recipe_display.setItem(self.tableWidget_recipe_display.rowCount() - 1, 2, QTableWidgetItem(recipe.difficulty))
        self.tableWidget_recipe_display.setItem(self.tableWidget_recipe_display.rowCount() - 1, 3, QTableWidgetItem(str(recipe.prep_time + recipe.cook_time)))
        self.tableWidget_recipe_display.setItem(self.tableWidget_recipe_display.rowCount() - 1, 4,
                                                QTableWidgetItem(str(recipe.serve)))
        self.tableWidget_recipe_display.setItem(self.tableWidget_recipe_display.rowCount() - 1, 5, QTableWidgetItem(','.join(recipe.types)))
        self.tableWidget_recipe_display.setItem(self.tableWidget_recipe_display.rowCount() - 1, 6, QTableWidgetItem(','.join(recipe.tags)))

    def _del_recipe(self):
        selected_recipes = self.tableWidget_recipe_display.selectedItems()
        if len(selected_recipes) > 0:
            if self._showDialog_delete_recipe():
                for recipe in selected_recipes:
                    if type(recipe) == RecipeTableItem:
                        self.cookbook.remove_recipe(recipe.recipe)
                        self.tableWidget_recipe_display.removeRow(self.tableWidget_recipe_display.row(recipe))

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
        self.search_recipes()

    def _add_recipe(self):
        self.edit_recipe_pop = EditRecipePopup()
        self.edit_recipe_pop.updated_recipe.connect(self.add_recipe_to_list)

    def add_recipe_to_list(self, recipe_dict: dict):
        self.edit_recipe_pop = None
        self.cookbook.append(recipe_dict)
        self.search_recipes()

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
        self.update_recipe_table()


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
        self.search_filter = []
        self.search_filter += self.generic_get_filter("recipe_name",
                                                 self.lineEdit_recipe_name_seach,
                                                 self.listWidget_recipe_name_selection)

        self.search_filter += self.generic_get_filter("recipe_author",
                                                 self.lineEdit_recipe_author_name_search,
                                                 self.listWidget_recipe_author_selection)

        self.search_filter += self.generic_get_filter("recipe_tag",
                                                 self.lineEdit_recipe_tag_search,
                                                 self.listWidget_recipe_tag_selection)

        self.search_filter += self.generic_get_filter("recipe_type",
                                                 self.lineEdit_recipe_type_search,
                                                 self.listWidget_recipe_type_selection)

        self.search_filter += self.generic_get_filter("recipe_difficulty",
                                                 self.lineEdit_recipe_dificulty_search,
                                                 self.listWidget_recipe_difficulty_selection)

        self.search_filter += self.generic_get_filter("ingredient_name",
                                                 self.lineEdit_ingredient_name_search,
                                                 self.listWidget_recipe_ingredient_name_selection)

        self.search_filter += self.generic_get_filter("ingredient_type",
                                                 self.lineEdit_ingredient_type_search,
                                                 self.listWidget_recipe_ingredient_type_selection)

        self.search_filter += self.generic_get_filter("ingredient_season",
                                                 self.lineEdit_ingredient_season_search,
                                                 self.listWidget_recipe_ingredient_season_selection)

        if self.horizontalSlider_prep_time_filter.value() != self.cookbook.longest:
            self.search_filter.append({"search_mode": "recipe_duration", "key": str(self.horizontalSlider_prep_time_filter.value())})

        print(self.search_filter)
        if len(self.search_filter) == 0:
            self.filtered_recipes = self.cookbook.recipe_list
        else:
            self.filtered_recipes = self.cookbook.find(self.search_filter)

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

# ===============================================================================
# Meal planner
# ================
    def _init_meal_planner(self):
        self._init_recipe_selection_table()
        self.init_ingredient_view_table()

    def _init_recipe_selection_table(self):
        # clear the table
        self.tableWidget_meal_planner_recipes.setColumnCount(6)
        self.tableWidget_meal_planner_recipes.setHorizontalHeaderLabels(["Name", "Servings", "Difficulty", "Prep Time",
                                                                         "Type", "Tag"])
        self.tableWidget_meal_planner_recipes.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_meal_planner_recipes.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget_meal_planner_recipes.setSortingEnabled(False)
        self.tableWidget_recipe_display.setWordWrap(True)

    def init_ingredient_view_table(self):
        self.tableWidget_ingredient_view.setColumnCount(3)
        self.tableWidget_ingredient_view.setHorizontalHeaderLabels(["Name", "Quantity", "Unit"])
        self.tableWidget_ingredient_view.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_ingredient_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)#QHeaderView.Stretch)
        self.tableWidget_ingredient_view.setSortingEnabled(False)
        self.tableWidget_recipe_display.setWordWrap(True)

    def add_manual_search_result(self):
        selected_recipes = self.tableWidget_recipe_display.selectedItems()
        for recipe in selected_recipes:
            if type(recipe) == RecipeTableItem:
                new_item = SearchResultTableItem(recipe.recipe, "manual", self.spinBox_servings_selector.value())
                self.generic_add_search_result_line(new_item, self.tableWidget_meal_planner_recipes)
        self.update_planer_info_view()

    def add_parametric_search_result(self):
        selected_recipes = sample(self.filtered_recipes, self.spinBox_quantity_selector.value())
        for recipe in selected_recipes:
                new_item = SearchResultTableItem(recipe, "auto", self.spinBox_servings_selector.value(), search_form=list(self.search_filter))
                self.generic_add_search_result_line(new_item, self.tableWidget_meal_planner_recipes)
        self.update_planer_info_view()

    def generic_add_search_result_line(self, new_item: SearchResultTableItem, table_widget):
        table_widget.insertRow(table_widget.rowCount())
        table_widget.setItem(table_widget.rowCount() - 1, 0, new_item)
        table_widget.setItem(table_widget.rowCount() - 1, 1, QTableWidgetItem(str(new_item.servings)))
        table_widget.setItem(table_widget.rowCount() - 1, 2, QTableWidgetItem(new_item.recipe.difficulty))
        table_widget.setItem(table_widget.rowCount() - 1, 3, QTableWidgetItem(str(new_item.recipe.prep_time + new_item.recipe.cook_time)))
        table_widget.setItem(table_widget.rowCount() - 1, 4, QTableWidgetItem(','.join(new_item.recipe.types)))
        table_widget.setItem(table_widget.rowCount() - 1, 5, QTableWidgetItem(','.join(new_item.recipe.tags)))
        table_widget.resizeRowsToContents()

    def delete_selected_search_results(self):
        selected_recipes = self.tableWidget_meal_planner_recipes.selectedItems()
        for recipe in selected_recipes:
            if type(recipe) == SearchResultTableItem:
                self.tableWidget_meal_planner_recipes.removeRow(self.tableWidget_meal_planner_recipes.row(recipe))

    def re_shuffle_parametric_item(self):
        # TODO clean by using generic function
        selected_items = self.tableWidget_meal_planner_recipes.selectedItems()
        for item in selected_items:
            if type(item) == SearchResultTableItem:
                # if selected a manual recipe, we cannot do anything here so we pass
                if item.mode != "auto":
                    continue
                # if we have not filter, use all recipes
                if len(item.search_form) == 0:
                    # if we have more than one recipe try to get new one, if we have one recipe only, do not do anything
                    if len(self.cookbook.recipe_list) > 1:
                        filtered_recipe = choice(self.cookbook.recipe_list)
                        # check that we don't have the same, try again if we do
                        while filtered_recipe == item.recipe:
                            filtered_recipe = choice(self.cookbook.recipe_list)
                        item.recipe = filtered_recipe
                        item.setText(filtered_recipe.name)
                        self.tableWidget_meal_planner_recipes.setItem(self.tableWidget_meal_planner_recipes.row(item),
                                                                      1,
                                                                      QTableWidgetItem(str(item.servings)))
                        self.tableWidget_meal_planner_recipes.setItem(self.tableWidget_meal_planner_recipes.row(item),
                                                                      2,
                                                                      QTableWidgetItem(item.recipe.difficulty))
                        self.tableWidget_meal_planner_recipes.setItem(self.tableWidget_meal_planner_recipes.row(item),
                                                                      3,
                                                                      QTableWidgetItem(
                                                                          str(item.recipe.prep_time + item.recipe.cook_time)))
                        self.tableWidget_meal_planner_recipes.setItem(self.tableWidget_meal_planner_recipes.row(item),
                                                                      4,
                                                                      QTableWidgetItem(','.join(item.recipe.types)))
                        self.tableWidget_meal_planner_recipes.setItem(self.tableWidget_meal_planner_recipes.row(item),
                                                                      5,
                                                                      QTableWidgetItem(','.join(item.recipe.types)))
                else:
                    lot = self.cookbook.find(item.search_form)
                    # if we have more than one recipe try to get new one, if we have one recipe only, do not do anything
                    if len(lot) > 1:
                        filtered_recipe = choice(lot)
                        # check that we don't have the same, try again if we do
                        while filtered_recipe == item.recipe:
                            filtered_recipe = choice(lot)
                        item.recipe = filtered_recipe
                        item.setText(filtered_recipe.name)
                        self.tableWidget_meal_planner_recipes.setItem(self.tableWidget_meal_planner_recipes.row(item),
                                                                      1,
                                                                      QTableWidgetItem(str(item.servings)))
                        self.tableWidget_meal_planner_recipes.setItem(self.tableWidget_meal_planner_recipes.row(item),
                                                                      2,
                                                                      QTableWidgetItem(item.recipe.difficulty))
                        self.tableWidget_meal_planner_recipes.setItem(self.tableWidget_meal_planner_recipes.row(item),
                                                                      3,
                                                                      QTableWidgetItem(
                                                                          str(item.recipe.prep_time + item.recipe.cook_time)))
                        self.tableWidget_meal_planner_recipes.setItem(self.tableWidget_meal_planner_recipes.row(item),
                                                                      4,
                                                                      QTableWidgetItem(','.join(item.recipe.types)))
                        self.tableWidget_meal_planner_recipes.setItem(self.tableWidget_meal_planner_recipes.row(item),
                                                                      5,
                                                                      QTableWidgetItem(','.join(item.recipe.types)))
        self.update_planer_info_view()

    def update_planer_info_view(self):
        self.update_ingredient_view()
        self.update_search_form_view()

    def update_search_form_view(self):
        self.listWidget_search_form_view.clear()
        selected = self.tableWidget_meal_planner_recipes.selectedItems()
        for item in selected:
            if type(item) == SearchResultTableItem:
                gap = "    "
                self.listWidget_search_form_view.addItem("Recipe: " + item.text())
                # if we got a manual recipe
                if item.mode == "manual":
                    self.listWidget_search_form_view.addItem(gap + "- Manual selection")
                # if we have no search params
                elif len(item.search_form) == 0:
                    self.listWidget_search_form_view.addItem(gap + "- All recipes")
                else:
                    for param in item.search_form:
                        self.listWidget_search_form_view.addItem(gap + "- " + param["search_mode"] + " -> " + param["key"])
                self.listWidget_search_form_view.addItem("---------------------")

    def add_new_recipe_from_selection(self):
        selected_items = self.tableWidget_meal_planner_recipes.selectedItems()
        for item in selected_items:
            if type(item) == SearchResultTableItem:
                if item.mode == "manual":
                    continue
                else:
                    # if the search form is blanc
                    if len(item.search_form) == 0:
                        # if we have more than one recipe try to get new one, if we have one recipe only, do not do anything
                        if len(self.cookbook.recipe_list) > 1:
                            filtered_recipe = choice(self.cookbook.recipe_list)
                            # check that we don't have the same, try again if we do
                            while filtered_recipe == item.recipe:
                                filtered_recipe = choice(self.cookbook.recipe_list)
                            new_item = SearchResultTableItem(filtered_recipe, "auto", item.servings,
                                                             search_form=list(item.search_form))
                            self.generic_add_search_result_line(new_item, self.tableWidget_meal_planner_recipes)
                    else:
                        lot = self.cookbook.find(item.search_form)
                        # if we have more than one recipe try to get new one, if we have one recipe only, do not do anything
                        if len(lot) > 1:
                            filtered_recipe = choice(lot)
                            # check that we don't have the same, try again if we do
                            while filtered_recipe == item.recipe:
                                filtered_recipe = choice(lot)
                            new_item = SearchResultTableItem(filtered_recipe, "auto", item.servings,
                                                             search_form=list(item.search_form))
                            self.generic_add_search_result_line(new_item, self.tableWidget_meal_planner_recipes)

    def update_ingredient_view(self):
        self.update_aggregated_ingredient_list()
        self.tableWidget_ingredient_view.setRowCount(0)
        for ingredient in self.aggregated_ingredient_list:
            self.tableWidget_ingredient_view.insertRow(self.tableWidget_ingredient_view.rowCount())
            self.tableWidget_ingredient_view.setItem(self.tableWidget_ingredient_view.rowCount() - 1, 0, QTableWidgetItem(ingredient.name))
            self.tableWidget_ingredient_view.setItem(self.tableWidget_ingredient_view.rowCount() - 1, 1, QTableWidgetItem(str(ingredient.quantity)))
            self.tableWidget_ingredient_view.setItem(self.tableWidget_ingredient_view.rowCount() - 1, 2, QTableWidgetItem(ingredient.unit))
        self.tableWidget_ingredient_view.resizeRowsToContents()

    def update_aggregated_ingredient_list(self):
        self.aggregated_ingredient_list.clear()
        # make a single list of ingredient from all recipes.
        selected_recipes = self.tableWidget_meal_planner_recipes.selectedItems()
        # if recipes are selected, display for those, else display for all recipes in table
        if len(selected_recipes) > 0:
            for item in selected_recipes:
                if type(item) == SearchResultTableItem:
                    self.append_to_ingredient_list(item.recipe, item.servings)
        else:
            for row in range(self.tableWidget_meal_planner_recipes.rowCount()):
                item = self.tableWidget_meal_planner_recipes.item(row, 0)
                self.append_to_ingredient_list(item.recipe, item.servings)
        self.round_aggregated_ingredient_quantities()

    def append_to_ingredient_list(self, recipe: Recipe, serving: int):
        # define the amount of the ingredient we have to add
        serving_ratio = serving / recipe.serve
        # check if the ingredient already exist.
        for ingredient in recipe.ingredient_list:
            test = True
            for ing in self.aggregated_ingredient_list:
                # if ingredient name and unit are the same, then ingredient is the same
                if (ingredient.name == ing.name) and (ingredient.unit == ing.unit) and (ingredient.comment == ing.comment):
                    # add quantity from existing
                    ing.quantity += ingredient.quantity * serving_ratio
                    test = False
                    break
            if test:
                # if we get here, we did not find an already existing ingredient matching, thus we add one.
                new_ingredient = Ingredient(ingredient.quantity * serving_ratio, ingredient.unit, ingredient.food_item, ingredient.comment)
                self.aggregated_ingredient_list.append(new_ingredient)

    def round_aggregated_ingredient_quantities(self):
        # round the result
        for ingredient in self.aggregated_ingredient_list:
            ingredient.quantity = round(ingredient.quantity, 1)
