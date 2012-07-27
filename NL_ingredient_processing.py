from bs4 import BeautifulSoup
import glob
import nltk

import pprint
import json


tokenizer = None
tagger = None


def init_nltk():
    global tokenizer
    global tagger
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')
    tagger = nltk.UnigramTagger(nltk.corpus.brown.tagged_sents())


def tag(text):
    global tokenizer
    global tagger
    if not tokenizer:
        init_nltk()
    tokenized = tokenizer.tokenize(text)
    tagged = tagger.tag(tokenized)
    tagged.sort(lambda x,y:cmp(x[1],y[1]))
    return tagged

#parse ingredients from json file and get nouns
#nouns pick up things like sea and pinch....
recipes = glob.glob('recipes/*.json')

for count, file in enumerate(recipes):
    json_data = open(file)
    data = json.load(json_data)
    ingredsHash = data["ingredients"]
    for ingredient in ingredsHash:
        ingreds = ingredient["ingredient"]
        tagged = tag(ingreds)
        for words in tagged:
            if words[1] == 'NN':
                print words[0]
    json_data.close()
