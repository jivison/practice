import os


def update(filename="wordPool.csv"):
    os.system("rm -rf wordPool.csv")
    print("Getting newest version of the word spreadsheet...")
    os.system(f"wget -O {filename} 'https://docs.google.com/spreadsheets/d/1f0K1SQJ7ZcInRaMTs7ZWJ3i5l7i_HI2OzKQY9zbE4cw/export?format=csv&id=1f0K1SQJ7ZcInRaMTs7ZWJ3i5l7i_HI2OzKQY9zbE4cw&gid=0' > /dev/null")


update()