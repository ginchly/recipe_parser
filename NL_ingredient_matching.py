import glob
import json
from collections import Counter


#parse ingredients from json file and get nouns
#nouns pick up things like sea and pinch....
recipes = glob.glob('recipes/*.json')
ingredsList = []
for count, file in enumerate(recipes):
    json_data = open(file)
    data = json.load(json_data)
    ingredsHash = data["ingredients"]
    for ingredient in ingredsHash:
        ingreds = ingredient["ingredient"].split()
        for ingred in ingreds:
            ingredsList.append(ingred.encode('utf-8'))
    json_data.close()

ingredsCount = Counter(ingredsList)
#print ingredsCount
dest = 'ingredients.txt'
#'w' to overwrite, 'a' to append
fo = open(dest, 'w')
for key, value in ingredsCount.items():
    #print key.strip(',.'), ',', value
    fo.write("%s,%d\n" % (key.strip(',.:;'), value))
fo.close()
