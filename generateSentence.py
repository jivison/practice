# TODO create sentence templates (eg. determiner object place verb; descriptive adjective object adjective)

# Custom library that generates an organized pool of words based on CSV files
from generatePool import generate

import random
import os

# Library to deal with jamo
import hgtk 

# Generate the pool using the given CSV files
pool = generate(vocabCSVs=["infile.csv", "additionalVocab/names.csv"])

# Prints the meaning, pronunciation, and any notes of the given words
def print_word_meaning(words):
    return [f"\t{word['Hangul']}: {word['Meaning']}\t\t\t[{word['Pronunciation']}{', ' if word['Notes'] != '' else ''}\x1B[3m{word['Notes']}\x1B[23m]\n" for word in words]

# Determines if a word ends in a vowel based on its pronunciation
def determineVowelEnding(pronunciation):
    return True if pronunciation[-1:] in ["a", "e", "o", "i", "u"] else False

# Exactly what it says in the function name
def createAdjectiveFromDescribingVerb(verb, verbPronunciation):
    if not determineVowelEnding(verbPronunciation):
        return verb[:-1] + "은"
    else:
        verb = verb[:-1]
        last_letter = verb[-1]
        # You can't mutate tuples so turn it into a list, add the final letter, convert it into a tuple, and finally compose it
        # TODO put this into a function
        decomp = list(hgtk.letter.decompose(last_letter))
        decomp[2] = "ㄴ"
        return verb[:-1] + hgtk.letter.compose(*tuple(decomp))

# Generates a sentence
def createSentence(count=3, determiner=True):

    # Keeps track of how many sentences have been created
    index = 0

    while True:
        os.system("clear")
        print("Your sentence is:\n" + int(len("Your sentence is:")/2) * "ㅡ" + "\n")

        # Initialize some parts of the sentence that may or may not be including
        determiner = None
        desc_adjective = None

        # Determine whether there will be a determiner in the sentence
        if random.choice(range(10)) > 7:
            # Picks a random determiner from the pool
            determiner = random.choice(pool["determiner"])
        
        # Determine whether there will be a descriptive adjective in the sentence
        if random.choice(range(11)) > 1:

            # Create a new entry for the descriptive adjective with update Notes, Meaning, Pronunciation, and Hangul
            desc_adjective = random.choice(pool["adjective"]).copy()
            desc_adjective["Meaning"] = desc_adjective["Meaning"].replace("to be", "").strip()
            desc_adjective["Hangul"] = createAdjectiveFromDescribingVerb(desc_adjective["Hangul"], desc_adjective["Pronunciation"][:-2])
            desc_adjective["Pronunciation"] = desc_adjective["Pronunciation"][:-2] + "n" if determineVowelEnding(desc_adjective["Pronunciation"]) else "eun"
            desc_adjective["Notes"] += "; shortened to a descriptive form" if desc_adjective["Notes"] != "" else "shortened to a descriptive form"

        # Picks a subject and an adjective from the pool
        subject = random.choice(pool["noun"])
        adjective = random.choice(pool["adjective"])

        # Creates the sentence
        print((f'{determiner["Hangul"]} ' if determiner != None else "") + (f'{desc_adjective["Hangul"]} ' if desc_adjective != None else "") + subject["Hangul"] + " " + adjective["Hangul"])
        input()
        # Prints the meanings etc. of all the words in the sentence
        print("Words used in this sentence:\n")
        print(f"{print_word_meaning([determiner])[0]}" if determiner != None else "", end="")
        print(f"{print_word_meaning([desc_adjective])[0]}" if desc_adjective != None else "", end="")
        print(f"{''.join(print_word_meaning([subject, adjective]))}")
        input()

        index += 1

        if index == count:
            break


createSentence(None)