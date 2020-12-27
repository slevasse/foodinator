from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import ingredient
from recipe import recipe
import logging
from tag_definition import recipe_tags
from ingredient import ingredient
from custom_table_items import ingredient_table_item
from tag_definition import recipe_tags


class editRecipePopup(QWidget):
#==========================
# Custom signals
#==========================
    updated_recipe = pyqtSignal(recipe)
#==========================
# Initialise widget
#==========================
    def __init__(self, recipe):
        super().__init__()
        uic.loadUi('edit_recipe.ui', self)
        self.tag_index = 0
        self.ingredient_index = 0
        self.type_index = 0
        self.recipe = recipe
        # load the recipe onscreen
        self.lineEdit_edit_name.setText(recipe._name)
        self.spinBox_edit_prep_time.setValue(recipe._meta_data['preptime'])
        self.spinBox_edit_cook_time.setValue(recipe._meta_data['cooktime'])
        self.spinBox_edit_portion.setValue(recipe._meta_data['serve'])
        self.set_tags(recipe._meta_data['tags'])
        self.set_meal_types(recipe._meta_data['type'])
        self.set_ingredients(recipe._ingredient_list)
        self.plainTextEdit_edit_instruction.setPlainText(recipe._instruction)
        # connects signals to callbacks
        self.pushButton_save.clicked.connect(self.save_recipe)
        self.pushButton_remove_selected_tags.clicked.connect(self.delete_tags)
        self.pushButton_add_tags.clicked.connect(self.add_tags_popup)
        self.show()

#==========================
# Save the modified data
#==========================
    def save_recipe(self):
        # name
        self.recipe._name = self.lineEdit_edit_name.text()
        # times
        self.recipe._meta_data['preptime'] = self.spinBox_edit_prep_time.value()
        self.recipe._meta_data['cooktime'] = self.spinBox_edit_cook_time.value()
        # serve
        self.recipe._meta_data['serve'] = self.spinBox_edit_portion.value()
        # ingredients
        # tags
        self.recipe._meta_data['tags'] = []
        for row in range(self.listWidget_edit_tags.count()):
            self.recipe._meta_data['tags'].append(self.listWidget_edit_tags.item(row).text())
        # type
        # instructions
        self.recipe._instruction = self.plainTextEdit_edit_instruction.toPlainText()
        self.updated_recipe.emit(self.recipe)
        self.close()

#==========================
# edit tags
#==========================
    def add_tags_popup(self):
        self.popup = QWidget()
        uic.loadUi('add_tags.ui', self.popup)
        self.popup.pushButton_add.clicked.connect(self.add_tags_2_recipe)
        # look at the tags present in the original list and only add the one missing to the new list
        for tag in recipe_tags().tags:
            match = False
            for row in range(self.listWidget_edit_tags.count()):
                if tag == self.listWidget_edit_tags.item(row).text():
                    match = True
                    break
            if not match:
                self.popup.listWidget_add.addItem(tag)
        self.popup.show()

    def add_tags_2_recipe(self):
        # get selected tags
        selected_tags = self.popup.listWidget_add.selectedItems()
        # add them to the tag list
        for tag in selected_tags:
            self.listWidget_edit_tags.addItem(tag.text())
        new_tag_list = []
        # close the popups
        self.popup.close()

    def delete_tags(self):
        # get selected tags
        selected_tags = self.listWidget_edit_tags.selectedItems()
        # for each tag, remove from the list
        for tag in selected_tags:
            self.listWidget_edit_tags.takeItem(self.listWidget_edit_tags.row(tag))

#==========================
# display the initial data
#==========================
    def set_tags(self, tags):
        for tag in tags:
            self.listWidget_edit_tags.insertItem(self.tag_index, tag)
            self.tag_index = self.tag_index +1


    def set_ingredients(self, ingredients):
        self.tableWidget_edit_ingredient.clear()
        self.tableWidget_edit_ingredient.setColumnCount(5)
        self.tableWidget_edit_ingredient.setHorizontalHeaderLabels(["Name", "Quantity", "Unit", "Type", "Season"])
        self.tableWidget_edit_ingredient.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_edit_ingredient.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for ing in ingredients:
            self.insert_ingredient(ing)
        self.show()


    def insert_ingredient(self, ing):
        self.tableWidget_edit_ingredient.insertRow(self.ingredient_index)
        self.tableWidget_edit_ingredient.setItem(self.ingredient_index,0, ingredient_table_item(ing))
        self.tableWidget_edit_ingredient.setItem(self.ingredient_index,1, QTableWidgetItem(str(ing.quantity)))
        self.tableWidget_edit_ingredient.setItem(self.ingredient_index,2, QTableWidgetItem(str(ing.unit)))
        self.tableWidget_edit_ingredient.setItem(self.ingredient_index,3, QTableWidgetItem(str(ing.type)))
        self.tableWidget_edit_ingredient.setItem(self.ingredient_index,4, QTableWidgetItem(str(ing.season)))
        self.ingredient_index = self.ingredient_index + 1


    def set_meal_types(self, types):
        for type in types:
            self.listWidget_edit_type.insertItem(self.type_index, type)
            self.type_index = self.type_index +1
