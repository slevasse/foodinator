from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import ingredient
from recipe import recipe
from ingredient import ingredient
import logging
from custom_table_items import ingredient_table_item

class newIngredientPopup(QWidget):
#==========================
# Custom signals
#==========================
    updated_ingredients = pyqtSignal(list)
#==========================
# Initialise widget
#==========================
    def __init__(self):
        # setup the window
        super().__init__()
        uic.loadUi('add_ingredient_popup.ui', self)
        self.pushButton_add_ingredient.clicked.connect(self.add_ingredient_button_clicked)
        self.pushButton_remove_ingredient.clicked.connect(self.pushButton_remove_ingredient_clicked)
        self.pushButton_save.clicked.connect(self.save_ingredient_list)
        self.ingredient_list = []
        # setup the table
        self.row = -1
        self.tableWidget_ingredient_list.clear()
        self.tableWidget_ingredient_list.setColumnCount(5)
        self.tableWidget_ingredient_list.setHorizontalHeaderLabels(["Name", "Quantity", "Unit", "Type", "Season"])
        self.tableWidget_ingredient_list.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_ingredient_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.show()

    def add_ingredient_button_clicked(self):
        # Add a new row
        self.row = self.row + 1
        self.tableWidget_ingredient_list.insertRow(self.row)
        # add data to table
        new_ingredient = ingredient(self.lineEdit_ingredient_name.text(),
                                    self.spinBox_quantity.value(),
                                    self.comboBox_unit.currentText(),
                                    self.comboBox_type.currentText(),
                                    self.comboBox_season.currentText())

        self.tableWidget_ingredient_list.setItem(self.row,0, ingredient_table_item(new_ingredient))
        self.tableWidget_ingredient_list.setItem(self.row,1, QTableWidgetItem(str(new_ingredient.quantity)))
        self.tableWidget_ingredient_list.setItem(self.row,2, QTableWidgetItem(new_ingredient.unit))
        self.tableWidget_ingredient_list.setItem(self.row,3, QTableWidgetItem(new_ingredient.type))
        self.tableWidget_ingredient_list.setItem(self.row,4, QTableWidgetItem(new_ingredient.season))


    def pushButton_remove_ingredient_clicked(self):
        self.row = self.row - 1
        selected_ingredients = self.tableWidget_ingredient_list.selectedItems()
        for ing in selected_ingredients:
            self.tableWidget_ingredient_list.removeRow(self.tableWidget_ingredient_list.row(ing))

    def save_ingredient_list(self):
        # add all to the ingredient list
        for row in range(0, self.tableWidget_ingredient_list.rowCount()):
            self.ingredient_list.append(self.tableWidget_ingredient_list.item(row,0).ingredient)
        # send a signal with the list of ingredients
        self.updated_ingredients.emit(self.ingredient_list)
        # close the window
        self.close()
