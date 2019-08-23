#!/usr/bin/python3

import updatePool
import numberPool
from difficulty import Difficulty

import json
import random
import datetime
import os
import math
import csv
from termcolor import colored

def safeDivision(num1, num2):
    if num2 == 0:
        return 0
    return math.ceil((num1/num2) * 100)


class Score():
    def __init__(self, filename):
        self.time = datetime.datetime.now()
        self.filename = filename
        self.score = {
            "correct": 0,
            "count": 0
        }
        self.difficulty = Difficulty("difficultWords.json")

    def get_avgScore(self):
        with open(self.filename, "r") as pointsfile:
            pointsreader = csv.DictReader(pointsfile)

            totalGamesPlayed = 0
            totalCount = []
            totalCorrect = []

            for line in pointsreader:
                totalGamesPlayed += 1
                totalCount.append(int(line["wordCount"]))
                totalCorrect.append(int(line["correct"]))

            return str(math.ceil((sum(totalCorrect) + self.score["correct"]) / (sum(totalCount) + self.score["count"]) * 100)), str(totalGamesPlayed) 

    def get_score(self):
        return str(safeDivision(self.score["correct"], self.score["count"]))


    def recordScore(self, msg, wordID):
        self.score["correct"] += self.difficulty.record(msg, wordID)
        self.score["count"] += 1


        return f"{msg}\nYour new score is {self.get_score()}%"


    def save(self):
        if self.score["count"] != 0:
            with open(self.filename, "a") as csvfile:
                csvfile.write(
                    f"{self.time}, {self.get_score()}, {self.score['count']}, {self.score['correct']}\n")


def 안녕(scoreObj):
    scoreObj.save()
    print("\n안영!")
    quit()


# random, Korean, or English (which language a given word is in)
def practice(pool, filename, title, givenLang="random"):

    idArray, idDict = pool[1], pool[0]
    
    score = Score(filename)

    score.difficulty.resetPool(idArray)

    random.shuffle(idArray)

    while True:

        os.system("clear")

        try:

            # Selecting
            # try:
            #     currentWordID = idArray.pop()
            #     currentWord = idDict[currentWordID]
            # except IndexError:
            #     print("There are no words left!")
            #     안녕(score)

            currentWordID, currentDifficulty = score.difficulty.getDifficultWord()
            currentWord = idDict[currentWordID]

            hints = [h for h in currentWord["hints"] if list(h.values())[
                0] != ""]
            random.shuffle(hints)

            currentWord = [currentWord["Korean"], currentWord["English"]]

            given, expected = None, None

            if givenLang == "random":
                given, expected = currentWord[
                    ::random.choice([1, -1])]
            else:
                given, expected = currentWord if givenLang == "Korean" else currentWord[::-1]

            given, expected = given.lower().strip(), expected.lower().strip()

            prhints = ""
            avgscore = ""

            # Displaying
            while True:

                os.system("clear")

                tempavg = score.get_avgScore()
                avgscore = "The total average score over {1} games is {0}%; you are currently {2}\n{3} words left".format(*tempavg, colored("better than average :)", "green") if int(tempavg[0]) <= int(score.get_score()) else colored("worse than average :(", "yellow"), len(idArray))
                
                messages = "\n".join([avgscore, prhints])

                userInput = input(f"\033[1m한국말 ({title})\033[0m\n{messages}\n({currentWordID}@{currentDifficulty}) {given}: ").lower()
                
                if userInput == ".quit" or userInput == ".벼샤":
                    안녕(score)

                elif userInput == ".amb" or userInput == ".므ㅠ":
                    try:
                        currentHint = hints.pop(0)
                        hints.append(currentHint)
                        newline = "\n"
                        prhints = f"Hint: {list(currentHint.keys())[0]} • {newline.join(list(currentHint.values())[0].split(';'))}"

                    except IndexError:
                        prhints = "No hints to show..."

                
                elif "." in userInput:
                    prhints = "Command not found (.quit, .amb)"

                else:
                    print(score.recordScore(
                        "Correct!" if userInput == expected else f"Incorrect, expected answer: {expected}", currentWordID)
                    )
                    if input() in ["c", "ㅊ"]:
                        score.score["correct"] += 1
                        score.difficulty.amend(currentWordID)
                        print(f"Correct? Your new score is {score.get_score()}%")
                        input()

                    break

        except KeyboardInterrupt:
            안녕(score)


practice(updatePool.generate(), "points.csv", "words")
# practice(numberPool.sinoKorean(99999), "numberPoints.csv", "numbers")