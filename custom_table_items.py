from PyQt5.QtWidgets import *
from foodClasses import *


class RecipeTableItem(QTableWidgetItem):
    def __init__(self, recipe: Recipe):
        super().__init__()
        self.setText(recipe.name)
        self.recipe = recipe


class IngredientTableItem(QTableWidgetItem):
    def __init__(self, ingredient: Ingredient):
        super().__init__()
        self.setText(ingredient.food_item['Name'])
        self.ingredient = ingredient


class FoodItemListItem(QListWidgetItem):
    def __init__(self, food_item: dict):
        super().__init__()
        self.setText(food_item['Name'])
        self.food_item = food_item


class SearchResultTableItem(QTableWidgetItem):
    def __init__(self, recipe: Recipe, mode: str, servings: int, search_form=None):
        super().__init__()
        self.setText(recipe.name)
        self.recipe: Recipe = recipe
        self.servings: int = servings
        self.mode: str = mode
        self.search_form: dict = search_form
