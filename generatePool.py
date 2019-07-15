import csv

# Generates a pool of words that can be sorted either once or twice
# It can take more than one csv file, in case vocab needs to be separated (eg. from different sources)

# Sorting structure:
# sort1:
#   secondary_sort1: <list of word dictionaries>
#   secondary_sort2: <list of word dictionaries>
# sort2:
#   secondary_sort3: <list of word dictionaries>

def generate(sort="Speech Part", vocabCSVs=['infile.csv'], secondary_sort=None):

    # The dictionary that will hold all the verbs
    output = {} 

    # The CSV headers
    headers = ['Hangul', "Meaning", "Pronunciation", "Speech Part", "Classification", "Notes", "Unit.Lesson"]

    # Iterate through each csv file
    for vocabCSV in vocabCSVs:

        with open(vocabCSV, "r") as infile:

            wordreader = csv.DictReader(infile, headers)

            for word_row in wordreader:

                # Skip the header row
                if word_row["Hangul"] != "Hangul":
                    
                    # Focus is the element that is sorted, eg. for sort 'Speech Part' focus could be 'noun', or 'adjective'
                    focus = word_row[sort]
                    copy_dict = dict(word_row.copy())

                    # If it's only one level deep sorting
                    if not secondary_sort:
                        # If it doesn't exist create it, else append to it
                        if focus not in output:
                            output[focus] = [copy_dict]
                        else:
                            output[focus].append(copy_dict)

                    else:
                        # Same as focus but a level deeper
                        secondary_focus = word_row[secondary_sort]
                        secondary_copy_dict = copy_dict.copy()

                        # If it doesn't exist create it, else append to it (but with another level) 
                        if focus not in output:
                            output[focus] = {
                                secondary_focus : [secondary_copy_dict]
                            }

                        elif secondary_focus not in output[focus]:
                            output[focus][secondary_focus] = [secondary_copy_dict]

                        else:
                            output[focus][secondary_focus].append(secondary_copy_dict)

    return output

# Make the outut look pretty, mainly for testing
def prettyprintwords(words, secondarySort=False):
    if secondarySort:
        for upper_focus, upper_listOfWords in words.items():
            print(upper_focus + ":")
            for lower_focus, lower_listOfWords in upper_listOfWords.items():
                print("\t" + lower_focus + ":")
                for word in lower_listOfWords:
                    print(f"\t\t{word['Hangul']}: {word['Meaning']}\t\t\x1B[3m{word['Notes']}\x1B[23m")
    
    else:
        for focus, listOfWords in words.items():
            print(focus + ":")
            for word in listOfWords:
                    print(f"\t{word['Hangul']}: {word['Meaning']}\t\t\x1B[3m{word['Notes']}\x1B[23m")

# _words = generate(sort="Unit.Lesson", secondary_sort="Speech Part")
# prettyprintwords(_words, True)