from PyQt5 import uic
from PyQt5.QtCore import *
from foodClasses import *
from food_item_library.foodLibrary import *
from custom_table_items import *

class EditRecipePopup(QWidget):
#==========================
# Custom signals
#==========================
    updated_recipe = pyqtSignal(dict)
#==========================
# Initialise widget
#==========================

    def __init__(self, recipe: Recipe = None):
        super().__init__()
        uic.loadUi('edit_recipe.ui', self)
        self.init_difficulty()
        self.foodLibrary = FoodLibrary()
        self.fooditem_index = 0
        self.tag_index = 0
        self.ingredient_index = 0
        self.type_index = 0
        if recipe is None:
            self.recipe = Recipe()
        elif isinstance(recipe, Recipe):
            self.recipe = recipe
        # load the recipe onscreen
        self._update_display()
        # connects signals to callbacks
        self.pushButton_remove_selected_ingredients.clicked.connect(self.remove_selected_ingredient)
        self.lineEdit_ingredient_search.textChanged.connect(self.update_ingredient_selector)
        self.listWidget_ingredient_search_result.itemDoubleClicked.connect(self.add_ingredient)
        self.pushButton_save_recipe.clicked.connect(self.save_recipe)
        self.show()

#==========================
# Set up the display
#==========================

    def _update_display(self):
        self.lineEdit_recipe_name.setText(self.recipe.name)
        self.lineEdit_author_name.setText(self.recipe.author)
        self.spinBox_recipe_prep_time.setValue(self.recipe.prep_time)
        self.spinBox_recipe_cook_time.setValue(self.recipe.cook_time)
        self.spinBox_recipe_portion.setValue(self.recipe.serve)
        self.set_difficulty(self.recipe.difficulty)
        self.set_tags(self.recipe.tags)
        self.set_meal_types(self.recipe.types)
        self.set_ingredients()
        self.plainTextEdit_recipe_instruction.setPlainText(self.recipe.instruction)
        # ingredient selector
        self.init_ingredient_selector()

    def init_difficulty(self):
        self.comboBox_difficulty_selector.addItems(Definitions().difficulties)

    def set_difficulty(self, dif: str):
        ind = self.comboBox_difficulty_selector.findText(dif)
        if ind > -1:
            self.comboBox_difficulty_selector.setCurrentIndex(ind)
        else:
            self.comboBox_difficulty_selector.setCurrentIndex(0)

    def set_tags(self, tags: list[str]):
        for def_tag in Definitions().tags:
            self.listWidget_recipe_tags.insertItem(self.type_index, def_tag)
            self.tag_index += 1
        for tag in tags:
            for ind in range(self.tag_index):
                if tag == self.listWidget_recipe_tags.item(ind).text():
                    self.listWidget_recipe_tags.item(ind).setSelected(True)

    def set_meal_types(self, types: list[str]):
        for def_type in Definitions().types:
            self.listWidget_recipe_types.insertItem(self.type_index, def_type)
            self.type_index += 1
        for typ in types:
            for ind in range(self.type_index):
                if typ == self.listWidget_recipe_types.item(ind).text():
                    self.listWidget_recipe_types.item(ind).setSelected(True)

    def set_ingredients(self):
        self.ingredient_index = 0
        self.tableWidget_recipe_ingredient.clear()
        self.tableWidget_recipe_ingredient.setColumnCount(5)
        self.tableWidget_recipe_ingredient.setHorizontalHeaderLabels(["Name", "Quantity", "Unit", "Type", "Season"])
        self.tableWidget_recipe_ingredient.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_recipe_ingredient.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.insert_ingredients()

    def insert_ingredients(self):
        for ing in self.recipe.ingredient_list:
            self.insert_single_ingredient(ing)

    def insert_single_ingredient(self, ingredient: Ingredient):
        self.tableWidget_recipe_ingredient.insertRow(self.ingredient_index)
        self.tableWidget_recipe_ingredient.setItem(self.ingredient_index, 0, IngredientTableItem(ingredient))
        self.tableWidget_recipe_ingredient.setItem(self.ingredient_index, 1, QTableWidgetItem(str(ingredient.quantity)))
        self.tableWidget_recipe_ingredient.setItem(self.ingredient_index, 2, QTableWidgetItem(str(ingredient.unit)))
        self.tableWidget_recipe_ingredient.setItem(self.ingredient_index, 3, QTableWidgetItem(str(ingredient.food_item['Type'])))
        self.tableWidget_recipe_ingredient.setItem(self.ingredient_index, 4, QTableWidgetItem(str(ingredient.food_item['Season'])))
        self.ingredient_index += 1

    def add_ingredient(self):
        if self.doubleSpinBox_ingredient_quantity.value() > 0:
            selected_food_items = self.listWidget_ingredient_search_result.selectedItems()
            for item in selected_food_items:
                ingredient = Ingredient(quantity=self.doubleSpinBox_ingredient_quantity.value(),
                                        unit=self.comboBox_ingredient_unit.currentText(),
                                        food_item=item.food_item,
                                        comment=self.lineEdit_ingredient_comment.text())
                # if the ingredient already exist, just add the quanditie
                if not self.does_ingredient_exit(item.food_item):
                    self.insert_single_ingredient(ingredient)
                # if it already exist we override
                else:
                    for index in range(self.ingredient_index):
                        if self.tableWidget_recipe_ingredient.item(index, 0).ingredient.food_item['Name'] == item.food_item['Name']:
                            self.tableWidget_recipe_ingredient.removeRow(index)
                            self.ingredient_index -= 1
                            self.insert_single_ingredient(ingredient)
        else:
            self.showDialog("Cannot add ingredient if quantity is 0.")

    def does_ingredient_exit(self, item: dict):
        for index in range(self.ingredient_index):
            if self.tableWidget_recipe_ingredient.item(index, 0).ingredient.food_item['Name'] == item['Name']:
                return True
        return False

    def remove_selected_ingredient(self):
        selected_ingredients = self.tableWidget_recipe_ingredient.selectedItems()
        for ing in selected_ingredients:
            if isinstance(ing, IngredientTableItem):
                self.tableWidget_recipe_ingredient.removeRow(self.tableWidget_recipe_ingredient.row(ing))
                self.ingredient_index -= 1

    def init_ingredient_selector(self):
        self.update_ingredient_selector()
        self.comboBox_ingredient_unit.addItems(Definitions().units)

    def update_ingredient_selector(self):
        self.listWidget_ingredient_search_result.clear()
        self.fooditem_index = 0
        search_text = self.lineEdit_ingredient_search.text()
        if search_text == "":
            for item in self.foodLibrary:
                self.listWidget_ingredient_search_result.insertItem(self.fooditem_index, FoodItemListItem(item))
                self.fooditem_index += 1
        else:
            food_item_result_list = self.foodLibrary.find([{"search_mode": "item_name", "key": search_text}])
            for item in food_item_result_list:
                self.listWidget_ingredient_search_result.insertItem(self.fooditem_index, FoodItemListItem(item))
                self.fooditem_index += 1

    def save_recipe(self):
        if self.can_i_save_the_recipe():
            recipe_temp = Recipe()
            # name
            recipe_temp.name = self.lineEdit_recipe_name.text()
            # author
            recipe_temp.author = self.lineEdit_author_name.text()
            # difficulty
            recipe_temp.difficulty = self.comboBox_difficulty_selector.currentText()
            # times
            recipe_temp.prep_time = self.spinBox_recipe_prep_time.value()
            recipe_temp.cook_time = self.spinBox_recipe_cook_time.value()
            # serve
            recipe_temp.serve = self.spinBox_recipe_portion.value()
            # ingredients
            for row in range(0, self.tableWidget_recipe_ingredient.rowCount()):
                recipe_temp.append_ingredient(self.tableWidget_recipe_ingredient.item(row, 0).ingredient)
            # tags
            for item in self.listWidget_recipe_tags.selectedItems():
                recipe_temp.append_recipe_tag(item.text())
            # type
            for item in self.listWidget_recipe_types.selectedItems():
                recipe_temp.append_recipe_type(item.text())
            # instructions
            recipe_temp.instruction = self.plainTextEdit_recipe_instruction.toPlainText()
            recipe_temp._update_meta()
            self.recipe.from_dict(recipe_temp.dict)
            self.updated_recipe.emit(recipe_temp.dict)
            self.recipe = None
            self.close()
        else:
            self.showDialog("Cannot save recipe if fields are missing.")

    def can_i_save_the_recipe(self):
        test = True
        if len(self.listWidget_recipe_tags.selectedItems()) == 0:
            test = False
        if len(self.listWidget_recipe_types.selectedItems()) == 0:
            test = False
        if self.tableWidget_recipe_ingredient.rowCount() == 0:
            test = False
        if (self.spinBox_recipe_prep_time.value() == 0) and (self.spinBox_recipe_cook_time.value() == 0):
            test = False
        if self.spinBox_recipe_portion.value() == 0:
            test = False
        if len(self.lineEdit_recipe_name.text()) == 0:
            test = False
        if len(self.lineEdit_author_name.text()) == 0:
            test = False
        return test

    def showDialog(self, text: str):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(text)
        msgBox.setWindowTitle("Warning")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

