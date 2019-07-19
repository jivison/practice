# TODO create sentence templates (eg. determiner object place verb; descriptive adjective object adjective)

# Custom library that generates an organized pool of words based on CSV files
import generatePool as pool
import generateStructurePool as structurePool
from callbacks import Callbacks

import random
import os

# Library to deal with jamo
import hgtk 

# Generate the pool using the given CSV files
NOFILTERPOOL, POOL = pool.generate(vocabCSVs=["infile.csv", "additionalVocab/names.csv"], secondary_sort="Classification")
STRUCTUREPOOL = structurePool.generate()

c = Callbacks()
defaultCharts = [c.tenseChart, c.formalityChart]


# Prints the meaning, pronunciation, and any notes of the given words
def print_word_meaning(words):
    [print(f"\t{word['Hangul']}: {word['Meaning']}\t\t\t[{word['Speech Part']}{', ' if word['Notes'] != '' else ''}\x1B[3m{word['Notes']}\x1B[23m]") for word in words]

# Generates a sentence
def createSentence(count=1):

    # Keeps track of how many sentences have been created
    index = 0

    while True:
        os.system("clear")
        print("Your sentence is:\n" + int(len("Your sentence is:")/2) * "ㅡ" + "\n")


        structure = random.choice(STRUCTUREPOOL)

        words = []

        for component in structure:
            options = component["options"]
            
            
            speechPart = component["speechPart"]

            try:
                if speechPart[1] == "subject":
                    options = random.choice([{"callback" : {"name" : "subject"}}, {"callback" : {"name" : "topic"}}])
                
                elif speechPart[1] == "object":
                    options = {"callback" : {"name" : "_object"}}

                elif speechPart[1] == "topic":
                    options = {"callback" : {"name" : "topic"}}

            except Exception as e:
                pass

            component["options"] = options

            if options == None:
                words.append(random.choice(NOFILTERPOOL[speechPart[0]]))

            else:
                if "filter" in options.keys():
                    choice = random.choice(POOL[speechPart[0]][options["filter"]])
                else:
                    choice = random.choice(NOFILTERPOOL[speechPart[0]])
                
                if "callback" not in options.keys():
                    pass
                elif options["callback"]["name"] in ["conjugate", "adjConjugate"]:
                    choice["Hangul"] = getattr(c, options["callback"]["name"])(choice["Hangul"], choice["Pronunciation"], random.choice(c.formalities), random.choice(c.tenses),defaultCharts)
                else:
                    choice["Hangul"] = getattr(c, options["callback"]["name"])(choice["Hangul"], choice["Pronunciation"])
                
                words.append(choice)

        for word in words:
            print(word["Hangul"], end=" ")

        input("\n")

        print_word_meaning(words)

        input()

        index += 1

        if index == count:
            break


createSentence(None)