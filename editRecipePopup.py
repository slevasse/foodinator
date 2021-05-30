from PyQt5 import uic
from PyQt5.QtCore import *
from foodClasses import *
from custom_table_items import *

class EditRecipePopup(QWidget):
#==========================
# Custom signals
#==========================
    updated_recipe = pyqtSignal(Recipe)
#==========================
# Initialise widget
#==========================

    def __init__(self, recipe: Recipe = None):
        super().__init__()
        uic.loadUi('edit_recipe.ui', self)
        self.init_difficulty()
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
        #self.pushButton_remove_selected_ingredients.clicked.connect(self.remove_selected_ingredient)
        #self.pushButton_save_recipe.clicked.connect(self.save_recipe)
        self.show()

#==========================
# Save the modified data
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
        self.set_ingredients(self.recipe.ingredient_list)
        self.plainTextEdit_recipe_instruction.setPlainText(self.recipe.instruction)

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

    def set_ingredients(self, ingredients: list[Ingredient]):
        self.tableWidget_recipe_ingredient.clear()
        self.tableWidget_recipe_ingredient.setColumnCount(5)
        self.tableWidget_recipe_ingredient.setHorizontalHeaderLabels(["Name", "Quantity", "Unit", "Type", "Season"])
        self.tableWidget_recipe_ingredient.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_recipe_ingredient.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for ing in ingredients:
            self.insert_ingredient(ing)

    def insert_ingredient(self, ing: Ingredient):
        self.tableWidget_recipe_ingredient.insertRow(self.ingredient_index)
        self.tableWidget_recipe_ingredient.setItem(self.ingredient_index,0, IngredientTableItem(ing))
        self.tableWidget_recipe_ingredient.setItem(self.ingredient_index,1, QTableWidgetItem(str(ing.quantity)))
        self.tableWidget_recipe_ingredient.setItem(self.ingredient_index,2, QTableWidgetItem(str(ing.unit)))
        self.tableWidget_recipe_ingredient.setItem(self.ingredient_index,3, QTableWidgetItem(str(ing.food_item['Type'])))
        self.tableWidget_recipe_ingredient.setItem(self.ingredient_index,4, QTableWidgetItem(str(ing.food_item['Season'])))
        self.ingredient_index += 1

#     def save_recipe(self):
#         if self.can_i_save_the_recipe():
#             # name
#             self.recipe._name = self.lineEdit_edit_name.text()
#             # times
#             self.recipe._meta_data['preptime'] = self.spinBox_edit_prep_time.value()
#             self.recipe._meta_data['cooktime'] = self.spinBox_edit_cook_time.value()
#             # serve
#             self.recipe._meta_data['serve'] = self.spinBox_edit_portion.value()
#             # ingredients
#             self.recipe._ingredient_list = []
#             for row in range(0, self.tableWidget_edit_ingredient.rowCount()):
#                 new_ingredient = ingredient(self.tableWidget_edit_ingredient.item(row,0).text(),
#                                             int(self.tableWidget_edit_ingredient.item(row,1).text()),
#                                             self.tableWidget_edit_ingredient.item(row,2).text(),
#                                             self.tableWidget_edit_ingredient.item(row,3).text(),
#                                             self.tableWidget_edit_ingredient.item(row,4).text())
#                 self.recipe._ingredient_list.append(new_ingredient)
#             # tags
#             self.recipe._meta_data['tags'] = []
#             for row in range(self.listWidget_edit_tags.count()):
#                 self.recipe._meta_data['tags'].append(self.listWidget_edit_tags.item(row).text())
#             # type
#             self.recipe._meta_data['type'] = []
#             for row in range(self.listWidget_edit_types.count()):
#                 self.recipe._meta_data['type'].append(self.listWidget_edit_types.item(row).text())
#             # instructions
#             self.recipe._instruction = self.plainTextEdit_edit_instruction.toPlainText()
#             self.updated_recipe.emit(self.recipe)
#             self.close()
#         else:
#             self.showDialog()
#
#     def can_i_save_the_recipe(self):
#         test = True
#         if self.listWidget_edit_tags.count() == 0:
#             test = False
#         if self.listWidget_edit_types.count() == 0:
#             test = False
#         if self.tableWidget_edit_ingredient.rowCount() == 0:
#             test = False
#         if (self.spinBox_edit_prep_time.value() == 0) and (self.spinBox_edit_cook_time.value() == 0):
#             test = False
#         if self.spinBox_edit_portion.value() == 0:
#             test = False
#         if len(self.lineEdit_edit_name.text()) == 0:
#             test = False
#         return test
#
#     def showDialog(self):
#         msgBox = QMessageBox()
#         msgBox.setIcon(QMessageBox.Warning)
#         msgBox.setText("Cannot save recipe if fields are missing.")
#         msgBox.setWindowTitle("Warning")
#         msgBox.setStandardButtons(QMessageBox.Ok)
#         msgBox.exec()
#
# #==========================
# # edit tags
# #==========================
#     def add_tags_popup(self):
#         self.popup = QWidget()
#         uic.loadUi('add_tags.ui', self.popup)
#         self.popup.pushButton_add.clicked.connect(self.add_tags_2_recipe)
#         # look at the tags present in the original list and only add the one missing to the new list
#         for tag in recipe_defs().tags:
#             match = False
#             for row in range(self.listWidget_edit_tags.count()):
#                 if tag == self.listWidget_edit_tags.item(row).text():
#                     match = True
#                     break
#             if not match:
#                 self.popup.listWidget_add.addItem(tag)
#         self.popup.show()
#
#     def add_tags_2_recipe(self):
#         # get selected tags
#         selected_tags = self.popup.listWidget_add.selectedItems()
#         # add them to the tag list
#         for tag in selected_tags:
#             self.listWidget_edit_tags.addItem(tag.text())
#         # close the popups
#         self.popup.close()
#
#     def delete_tags(self):
#         # get selected tags
#         selected_tags = self.listWidget_edit_tags.selectedItems()
#         # for each tag, remove from the list
#         for tag in selected_tags:
#             self.listWidget_edit_tags.takeItem(self.listWidget_edit_tags.row(tag))
#
# #==========================
# # edit types
# #==========================
#     def add_type_popup(self):
#         self.popup = QWidget()
#         uic.loadUi('add_tags.ui', self.popup)
#         self.popup.pushButton_add.clicked.connect(self.add_types_2_recipe)
#         # look at the tags present in the original list and only add the one missing to the new list
#         for type in recipe_defs().types:
#             match = False
#             for row in range(self.listWidget_edit_types.count()):
#                 if type == self.listWidget_edit_types.item(row).text():
#                     match = True
#                     break
#             if not match:
#                 self.popup.listWidget_add.addItem(type)
#         self.popup.show()
#
#     def add_types_2_recipe(self):
#         # get selected tags
#         selected_types = self.popup.listWidget_add.selectedItems()
#         # add them to the tag list
#         for type in selected_types:
#             self.listWidget_edit_types.addItem(type.text())
#         # close the popups
#         self.popup.close()
#
#
#     def delete_types(self):
#         # get selected tags
#         selected_types = self.listWidget_edit_types.selectedItems()
#         # for each tag, remove from the list
#         for type in selected_types:
#             self.listWidget_edit_types.takeItem(self.listWidget_edit_types.row(type))
#
# #==========================
# # edit ingredients
# #==========================
#     def delete_ingredients(self):
#         selected_ingredients = self.tableWidget_edit_ingredient.selectedItems()
#         for ing in selected_ingredients:
#             self.tableWidget_edit_ingredient.removeRow(self.tableWidget_edit_ingredient.row(ing))
#
#
#     def add_ingredient_popup(self):
#         self.new_ingredient_popup = newIngredientPopup()
#         self.new_ingredient_popup.updated_ingredients.connect(self.add_2_ingredient_list)
#
#     def add_2_ingredient_list(self, ingredient_list):
#         for ing in ingredient_list:
#             self.insert_ingredient(ing)
#
#
# #==========================
# # display the initial data
# #==========================
#     def set_tags(self, tags):
#         for tag in tags:
#             self.listWidget_edit_tags.insertItem(self.tag_index, tag)
#             self.tag_index = self.tag_index +1
#
#
#     def set_ingredients(self, ingredients):
#         self.tableWidget_edit_ingredient.clear()
#         self.tableWidget_edit_ingredient.setColumnCount(5)
#         self.tableWidget_edit_ingredient.setHorizontalHeaderLabels(["Name", "Quantity", "Unit", "Type", "Season"])
#         self.tableWidget_edit_ingredient.horizontalHeader().setStretchLastSection(True)
#         self.tableWidget_edit_ingredient.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
#         for ing in ingredients:
#             self.insert_ingredient(ing)
#         self.show()
#
#
#     def insert_ingredient(self, ing):
#         self.tableWidget_edit_ingredient.insertRow(self.ingredient_index)
#         self.tableWidget_edit_ingredient.setItem(self.ingredient_index,0, ingredient_table_item(ing))
#         self.tableWidget_edit_ingredient.setItem(self.ingredient_index,1, QTableWidgetItem(str(ing.quantity)))
#         self.tableWidget_edit_ingredient.setItem(self.ingredient_index,2, QTableWidgetItem(str(ing.unit)))
#         self.tableWidget_edit_ingredient.setItem(self.ingredient_index,3, QTableWidgetItem(str(ing.type)))
#         self.tableWidget_edit_ingredient.setItem(self.ingredient_index,4, QTableWidgetItem(str(ing.season)))
#         self.ingredient_index = self.ingredient_index + 1
#
#
#     def set_meal_types(self, types):
#         for type in types:
#             self.listWidget_edit_types.insertItem(self.type_index, type)
#             self.type_index = self.type_index +1
