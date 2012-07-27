import glob
import json
import os
import csv

class Condiment:
    pass

def stripNonASCII(s):
    return "".join([c for c in s if ord(c) < 129])

#parse ingredients from json file and get nouns
#nouns pick up things like sea and pinch....
recipes = glob.glob('recipes/*.json')

with open('ingredients.csv', 'rU') as f:
    reader = csv.reader(f)

    masterIngreds = {}
    #split text file into array for matching
    for row in reader:
        name = stripNonASCII(row[0])
        if row[2] != "":  # plural form
            masterIngreds.update({name: stripNonASCII(row[2])})
        elif row[1] == "c":
            masterIngreds.update({name: Condiment})
        elif row[1] == "f":
            masterIngreds.update({name: None})
        else:
            raise Exception("Unexpected master ingredient format: {}".format(row))

for filename in recipes:
    coreIngreds = []
    with open(filename, 'r') as json_data:
        data = json.load(json_data)

    for ingredient in data["ingredients"]:
        # hack: remove non-ascii characters :(
        ingreds = stripNonASCII(ingredient["ingredient"])
        # find all master ingredients that are substrings of the recipe ingredient
        contained = [x for x in masterIngreds.keys() if x in ingreds]
        if contained:
            coreIngred = sorted(contained, key=len)[-1]  # if more than one match, take longest
            if masterIngreds[coreIngred] == Condiment:
                # ignore condiments! (but note we needed to find them here to ensure we got the true longest substring match)
                pass
            elif masterIngreds[coreIngred] == None: # a real singular food
                ingredient["coreIngred"] = coreIngred
            else: # must be a plural
                ingredient["coreIngred"] = masterIngreds[coreIngred]

    #overwrite updated json (with coreIngred added) to existing file
    with open("recipes/with_ingredients/{}".format(filename[8:]), 'w') as json_data:
        json_data.write(json.dumps(data))
