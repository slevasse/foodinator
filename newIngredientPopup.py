from PyQt5 import uic
from PyQt5.QtWidgets import *
import ingredient
from recipe import recipe
import logging

class newIngredientPopup(QWidget):
    def __init__(self, temp_recipe):
        # setup the window
        super().__init__()
        uic.loadUi('add_ingredient_popup.ui', self)
        self.pushButton_add_ingredient.clicked.connect(self.add_ingredient_button_clicked)
        self.pushButton_remove_ingredient.clicked.connect(self.pushButton_remove_ingredient_clicked)
        self.pushButton_add_all_to_recipe.clicked.connect(self.pushButton_add_all_to_recipe_clicked)
        #
        self.temp_recipe = temp_recipe
        # setup the table
        self.tableWidget_ingredient_list.setColumnCount(5)
        self.row = 0
        self.tableWidget_ingredient_list.insertRow(self.row)
        self.tableWidget_ingredient_list.setItem(self.row,0, QTableWidgetItem("Name"))
        self.tableWidget_ingredient_list.setItem(self.row,1, QTableWidgetItem("Quantity"))
        self.tableWidget_ingredient_list.setItem(self.row,2, QTableWidgetItem("Unit"))
        self.tableWidget_ingredient_list.setItem(self.row,3, QTableWidgetItem("Type"))
        self.tableWidget_ingredient_list.setItem(self.row,4, QTableWidgetItem("Season"))
        self.tableWidget_ingredient_list.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_ingredient_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.show()

    def add_ingredient_button_clicked(self):
        # add a new row
        self.row = self.row + 1
        self.tableWidget_ingredient_list.insertRow(self.row)
        # add data to table
        self.tableWidget_ingredient_list.setItem(self.row,0, QTableWidgetItem(self.lineEdit_ingredient_name.text()))
        self.tableWidget_ingredient_list.setItem(self.row,1, QTableWidgetItem(str(self.spinBox_quantity.value())))
        self.tableWidget_ingredient_list.setItem(self.row,2, QTableWidgetItem(self.comboBox_unit.currentText()))
        self.tableWidget_ingredient_list.setItem(self.row,3, QTableWidgetItem(self.comboBox_season.currentText()))
        self.tableWidget_ingredient_list.setItem(self.row,4, QTableWidgetItem(self.comboBox_type.currentText()))

    def pushButton_remove_ingredient_clicked(self):
        if (self.row > 0):
            self.tableWidget_ingredient_list.removeRow(self.row)
            self.row = self.row - 1

    def pushButton_add_all_to_recipe_clicked(self):
        # add all to the ingredient list
        for index in range(1, self.row+1):
            temp_ingredient = ingredient.ingredient(self.tableWidget_ingredient_list.takeItem(index, 0).text(),
                                                                int(self.tableWidget_ingredient_list.takeItem(index, 1).text()),
                                                                self.tableWidget_ingredient_list.takeItem(index, 2).text(),
                                                                self.tableWidget_ingredient_list.takeItem(index, 3).text(),
                                                                self.tableWidget_ingredient_list.takeItem(index, 4).text())
            #self.foodlist.add_ingredient(temp_ingredient)
            # add ingredients to the recipe
            self.temp_recipe.add_ingredient(temp_ingredient)
        # close the window
        self.close()
