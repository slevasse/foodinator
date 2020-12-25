from recipe import recipe
import json
import os.path
import logging

from ingredient import ingredient

ing_list = [ingredient("potato", 12, "unit", "veg", "autumn"), ingredient("banana", 5, "unit", "fruit", "summer")]
myrec = recipe("test", 3, {'preptime':120, 'cooktime':45, 'serve':6}, ing_list, "make it rain.", ["fresh", "baby"])
myrec2 = recipe("test", 3, {'preptime':120, 'cooktime':45, 'serve':6}, ing_list, "make it rain.", ["fresh", "baby"])

listo = [myrec, myrec2]
diclist = []
for obj in listo:
    diclist.append(obj.dictify())

dicted = myrec.dictify()

testo = {"recipe_list": [dicted, dicted, dicted]}

with open('ingredient_list_db.json', 'w') as outfile:
    json.dump(dicted, outfile, sort_keys=False, indent=4)

with open('recipe_list_db.json', 'w') as outfile:
    json.dump(testo, outfile,sort_keys=False, indent=4)




with open("recipe_list_db.jsn", "r") as read_file:
    # load the file as a dict
    data = json.load(read_file)
    #
    myrecipelist = []
    # iterate through the dict
    for a_recipe in data["recipe_list"]:
        # get the ingredients
        ingredient_list = []
        for a_ing in a_recipe["_ingredient_list"]:
            ingredient_list.append(ingredient(a_ing["name"],
                                              a_ing["quantity"],
                                              a_ing["unit"],
                                              a_ing["type"],
                                              a_ing["season"],))
        # write the new object list
        myrecipelist.append(recipe(a_recipe["_name"],
                                   a_recipe["_id"],
                                   a_recipe["_meta_data"],
                                   ingredient_list,
                                   a_recipe["_instruction"],
                                   a_recipe["_tags"]))
