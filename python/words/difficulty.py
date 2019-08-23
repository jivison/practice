import json
import random
import os

class Difficulty():
    def __init__(self, filename):
        # Schema: 
        # "words": {
        #   "word1ID" : [1, 1, 1]
        #   },
        #   "word2ID" : [0 , 1, 1]
        #   },
        # "sortedKeys" : {
        #   "3" : ["word1ID"],
        #   "2" : ["word2ID"]
        # }
        
        self.filename = filename

    def resetFile(self, jsonObj):
        os.system(f"rm {self.filename}")
        with open(self.filename, "w+") as diffs:
            json.dump(jsonObj, diffs)

    def readFile(self):
        with open(self.filename, "r") as diffs:
            return json.load(diffs)

    def resetPool(self, id_array):
        poolJson = {"words" : {}, "sortedKeys" : {0 : [], 1: [], 2: [], 3: []}}
        
        for wordID in id_array:
            poolJson["words"][wordID] = [0, 0, 0]
        
        self.resetFile(poolJson)

        self.regenPool()

    def regenPool(self):
        difficultyPool = self.readFile()

        for wordID, scoreRecord in difficultyPool["words"].items():
            
            difficultyPool["sortedKeys"][str(sum(scoreRecord))].append(wordID)

        self.resetFile(difficultyPool)

    def record(self, msg, wordID):
        correct = 1 if msg == "Correct!" else 0
        difficultyPool = self.readFile()
        difficultyPool["words"][wordID] = difficultyPool["words"][wordID][1:] 
        difficultyPool["words"][wordID].append(correct)

        self.resetFile(difficultyPool)

        return correct

    def getDifficultWord(self):
        self.regenPool()
        
        difficultyPool = self.readFile()
        wordIDArray = difficultyPool["sortedKeys"]

        if len(wordIDArray["0"]) > 0:
            wordIDArray = wordIDArray["0"]
        elif len(wordIDArray["1"]) > 0:
            wordIDArray = wordIDArray["1"]
        elif len(wordIDArray["2"]) > 0:
            wordIDArray = wordIDArray["2"]
        elif len(wordIDArray["3"]) > 0:
            wordIDArray = wordIDArray["3"]

        random.shuffle(wordIDArray)
        
        wordID = wordIDArray[0]
        difficulty = sum(difficultyPool["words"][wordID])
        
        return wordID, difficulty
        
    def amend(self, wordID):
        difficultyPool = self.readFile()
        difficultyPool["words"][wordID][2] = 1

        self.resetFile(difficultyPool)
    
    def updatePool():
        pass
