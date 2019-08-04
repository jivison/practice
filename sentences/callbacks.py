import hgtk

def determineVowelEnding(pronunciation):
    return True if pronunciation[-1] in ["a", "e", "o", "i", "u"] else False

def addFinalConsonant(hangeulChar, addingJamo):
        # You can't mutate tuples so turn it into a list, add the final letter, convert it into a tuple, and finally compose it
        decomp = list(hgtk.letter.decompose(hangeulChar))
        decomp[2] = addingJamo
        return hgtk.letter.compose(*tuple(decomp))

def merge(str1, str2):

    if str2 == "NONE":
        return str1
    else:

        lastChar = str1[-1]
        firstChar = str2[0]

        lastJamos = list(hgtk.letter.decompose(lastChar))
        firstJamos = list(hgtk.letter.decompose(firstChar))
        firstJamoscopy = firstJamos.copy()
        firstJamoscopy[2] = ""

        mergeChart = {
            "ㅏ + 아" : "ㅏ",
            "ㅗ + 아" : "ㅘ",
            "ㅜ + 어" : "ㅝ",
            "ㅣ + 어" : "ㅕ",
            "ㅓ + 어" : "ㅓ",
            "ㅕ + 어" : "ㅕ",
            "ㅏ + 여" : "ㅐ"
        }

        try:
            if lastJamos[-1] != "" or hgtk.letter.compose(*tuple(firstJamoscopy)) not in ["아", "이", "어", "우", "오", "여"]:
                return str1 + str2
            else:
                combination = f"{lastJamos[1]} + {hgtk.letter.compose(*tuple(firstJamoscopy))}"
                newChar = tuple([lastJamos[0], mergeChart[combination], firstJamos[2]])
                return str1[:-1] + hgtk.letter.compose(*newChar) + str2[1:]
        except:
            if lastJamos[-1] == "" and firstJamos[-2] == "" and str2 != "":
                return str1[:-1] + addFinalConsonant(lastChar, firstChar) + str2[1:]
            else:
                raise Exception("uhh idk fix merge in callback")

defaultCharts = []

class Callbacks():

    def __init__(self):
        self.formalityChart = {
            "lowInformal" : {"오, 아" : "아", "하" : "여", "else" : "어"},
            "highInformal" : {"오, 아" : "아요", "하" : "여요", "else" : "어요"},
            "highFormal" : {"vowel" : "ㅂ니다", "consonant" : "습니다"},
            "plainForm" : {"else" : "다"}
        }

        self.tenseChart = {                                                                  # Placeholder for nothing
            "present" : {"plainFormConsonant" : "는", "plainFormVowel" : "ㄴ", "else" : "NONE"},
            "future" : {"else" : "겠"}, 
            "past" : {"오, 아" : "았", "하" : "였", "else" : "었"}
        }

        self.formalities = list(self.formalityChart.keys())
        self.tenses = list(self.tenseChart.keys())

        self.adjectiveTenseChart = self.tenseChart
        self.adjectiveTenseChart["present"] = {"plainFormConsonant" : "NONE", "plainFormVowel" : "NONE", "else" : "NONE"}


    # Direct callback (from structure file)
    def adjConjugate(self, adjective, pronunciation, formality, tense, charts):
        return self.conjugate(adjective, pronunciation, formality, tense, charts=[self.adjectiveTenseChart, self.formalityChart])

    # Direct callback (from structure file)
    def conjugate(self, verb, pronunciation, formality, tense, charts=defaultCharts):
        t = charts[0]
        f = charts[1]
    
        verb = verb[:-1]
        pronunciation = pronunciation[:-2]

        lastChar = verb[-1]
        lastJamos = list(hgtk.letter.decompose(lastChar))
        
        formalityConj = None
        tenseConj = None

        # FORMALITY CONJUGATIONS
        if tense in ["present"]:
            if formality in ["lowInformal", "highInformal"]:
                if lastChar == "하":
                    formalityConj = f[formality]["하"]
                elif "ㅗ" in lastJamos or "ㅏ" in lastJamos:
                    formalityConj = f[formality]["오, 아"]
                else:
                    formalityConj = f[formality]["else"]
        
            elif formality in ["highFormal"]:
                if determineVowelEnding(pronunciation):
                    formalityConj = f[formality]["vowel"]
                else:
                    formalityConj = f[formality]["consonant"]

            elif formality in ["plainForm"]:
                formalityConj = f[formality]["else"]

        else:
            if formality in ["lowInformal", "highInformal", "plainForm"]:
                formalityConj = f[formality]["else"]
            elif formality in ["highFormal"]:
                formalityConj = f[formality]["consonant"]

            
        # TENSE CONJUGATIONS

        if formality in ["plainForm"] and tense in ["present"]:
            if determineVowelEnding(pronunciation):
                tenseConj = t[tense]["plainFormVowel"]
            else:
                tenseConj = t[tense]["plainFormConsonant"]

        elif tense in ["future", "present"]:
            tenseConj = t[tense]["else"]

        elif tense in ["past"]:
            if lastChar == "하":
                tenseConj = t[tense]["하"]
            elif "ㅗ" in lastJamos or "ㅏ" in lastJamos:
                tenseConj = t[tense]["오, 아"]
            else:
                tenseConj = t[tense]["else"]

        tensified = merge(verb, tenseConj)
        formalized = merge(tensified, formalityConj)

        return formalized

    # Direct callback (from structure file)
    def descriptive(self, adjective, pronunciation):
        if adjective[-2:] == "있다":
            adjective = adjective[:-1] + "는"

        else:
            pronunciation = pronunciation[:-2]
            if determineVowelEnding(pronunciation):
                adjective = adjective[:-2] + addFinalConsonant(adjective[-2], "ㄴ")
            else:
                adjective = adjective[:-1] + "은"


        return adjective

    # Indirect callback
    def topic(self, noun, pronunciation):
        if determineVowelEnding(pronunciation):
            noun = noun + "는"
        else:
            noun = noun + "은"
        
        return noun
    
    # Indirect callback
    def subject(self, noun, pronunciation):
        if determineVowelEnding(pronunciation):
            noun = noun + "가"
        else:
            noun = noun + "이"

        return noun

    # Indirect callback
    def _object(self, noun, pronunciation):
        if determineVowelEnding(pronunciation):
            noun = noun + "를"
        else:
            noun = noun + "을"

        return noun

    # Indirect callback
    def timeplace(self, noun, pronunciation):
        return noun + "에"



# adjective = "비싸다"
# pronunciation = "bissada"

# # High/Low Formal/Informal
# formality = "highFormal"

# print(c.conjugate(adjective, pronunciation, formality, "past", charts=defaultCharts))
# print(c.conjugate(adjective, pronunciation, formality, "present", charts=defaultCharts))
# print(c.conjugate(adjective, pronunciation, formality, "future", charts=defaultCharts))

