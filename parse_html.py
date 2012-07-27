from bs4 import BeautifulSoup
import glob
import os
import json


def getIngredients(soup):
        #on foodnetwork.co.uk, ingredients are li items with class 'ingredient item'
    ingredients = []
    for ingreds in soup.find_all('li', 'ingredient-item'):
        #separate quantity from actual ingredient
        if ingreds.string == None:  # sometimes we get an empty ingredient
            continue

        if ingreds.string[0].isdigit():
                ingredsSplit = ingreds.string.partition(' ')
                #first tuple is number, second is delimeter(space), third is ingredient
                ingredsQty = ingredsSplit[0]
                #make lower case to make matching easier
                ingred = ingredsSplit[2].lower()
        else:
            ingredsQty = ''
            ingred = ingreds.string.lower()

        coreIngred = ingred
        ingredients.append({'qty': ingredsQty, 'ingredient': coreIngred})
    return ingredients


def getMethod(soup):
    try:
        method = str(soup.find('div', {'id': 'method-box'}).contents)
    except Exception:
        method = ''

    return method


def getAttributes(soup):
    attributesDict = {}
    try:
        attributesDict['difficulty'] = soup.find('span', {'class': 'icons difficulty'}).next_sibling.next_sibling.string
    except AttributeError:
        pass
    try:
        attributesDict['serves'] = soup.find('strong', {'itemprop': 'recipeYield'}). string
    except AttributeError:
        pass
    #<span class="icons clock"></span>Prep time &rsaquo; <meta itemprop="cookTime" content="PT-22350091M">
                #<strong>&frac12; hr</strong>
    #encode to utf-8 to deal with fractions in time
    try:
        recipeTimes = soup.find_all('span', {'class': 'icons clock'})
        attributesDict['prepTime'] = recipeTimes[0].parent.find('strong').string.encode('utf-8')
        attributesDict['cookTime'] = recipeTimes[1].parent.find('strong').string.encode('utf-8')
    except IndexError:
        pass
    try:
        attributesDict['cuisine'] = soup.find('span', {'class': 'topic-button'}).string
    except AttributeError:
        pass

    try:
        attributesDict['img_url'] = soup.findAll('div', {'id': 'recipe-gallery'})[0].findAll('img')[0]['src']
    except:
        pass

    return attributesDict

def getTitle(file):
    recipePath = os.path.basename(file)
    recipeTitleSplit = recipePath.partition('.')
    recipeTitle = recipeTitleSplit[0].replace('-', ' ')
    return recipeTitle

#go through all files in recipe folder
#reference by recipe name (better for fuzzy matching) or hash
recipes = glob.glob('recipes/*.html')
skipExisting = True
for count, file in enumerate(recipes):
    # check if this has already been processed
    if skipExisting:
        try:
            with open("{}.json".format(file)) as f: pass
            continue  # it has already been processed
        except IOError as e:
            pass  # it doesn't exist, carry on

    with open(file, 'r') as html:
	    soup = BeautifulSoup(html.read())

    recipeIngredients = getIngredients(soup)
    recipeMethod = getMethod(soup)
    recipeTitle = getTitle(file)
    recipe = {'title': recipeTitle, 'ingredients': recipeIngredients, 'method': recipeMethod}
    recipe.update(getAttributes(soup))

    dest = "{}.json".format(file) 
    with open(dest, 'w') as outf:
	    outf.write(json.dumps(recipe))

    if (count % 10) == 0:
        print("Progress: {} of {}".format(count, len(recipes)))
