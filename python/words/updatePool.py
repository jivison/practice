import sys
import csv
import os


def update(filename="wordPool.csv"):
    os.system("rm -rf wordPool.csv")
    print("Getting newest version of the word spreadsheet...")
    os.system(f"wget -O {filename} 'https://docs.google.com/spreadsheets/d/1f0K1SQJ7ZcInRaMTs7ZWJ3i5l7i_HI2OzKQY9zbE4cw/export?format=csv&id=1f0K1SQJ7ZcInRaMTs7ZWJ3i5l7i_HI2OzKQY9zbE4cw&gid=0' > /dev/null")

    return filename


def generate():
    filename = update()
    # filename = "wordPool.csv"
    
    print("Generating word pool...")

    with open(filename, "r") as file:
        reader = csv.DictReader(file)

        _id = 0

        _idDict = {}
        _idArray = []

        for line in reader:
            _id += 1

            _idArray.append(f"word_{_id}")

            _idDict[f"word_{_id}"] = {
                "Korean" : line["Hangul"],
                "English" : line ["Meaning"],
                "hints" : [
                    {"speechPart" : line["Speech Part"]},
                    {"classificaion" : line["Classification"]},
                    {"additional" : line["Notes"]}
                    ]
                }
                

    
    return _idDict, _idArray
        
