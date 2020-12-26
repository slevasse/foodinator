from PyQt5 import uic
from PyQt5.QtWidgets import *
import ingredient
from recipe import recipe
import logging
from tag_definition import recipe_tags

class editRecipePopup(QWidget):
    def __init__(self, recipe):
        super().__init__()
        uic.loadUi('edit_recipe.ui', self)
        # load the recipe onscreen
        self.lineEdit_edit_name.setText(recipe._name)
        self.spinBox_edit_prep_time.setValue(recipe._meta_data['preptime'])
        self.spinBox_edit_cook_time.setValue(recipe._meta_data['cooktime'])
        self.spinBox_edit_portion.setValue(recipe._meta_data['serve'])
        self.plainTextEdit_edit_instruction.setPlainText(recipe._instruction)
        self.show()
