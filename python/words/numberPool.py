# Needs to be updated to the new pool system


def sinoKorean(max):

    print(f"Generating numbers to {max}")

    digits = {
        "0" : "",
        "1" : "일",
        "2" : "이",
        "3" : "삼",
        "4" : "사",
        "5" : "오",
        "6" : "육",
        "7" : "칠",
        "8" : "팔",
        "9" : "구",   
    }
    places = {
        "0" : "",
        "1" : "십",
        "2" : "백",
        "3" : "천",
        "4" : "만"
    }

    pool = []

    for n in range(1, max + 1):

        origN = n

        n = list(str(n))
        n.reverse()
        n = "".join(n)

        result = []

        for digit_i in range(len(str(n))):

            currentDig = n[digit_i]

            currentDig = "0" if (currentDig == "1" and digit_i > 0) else currentDig

            if currentDig == "0":
                digit_i = "0"
                

            # print(f"====> {currentDig}, {digit_i}")

            result.insert(0, digits[currentDig] + places[str(digit_i)])

        pool.append({"Korean" : "".join(result), "English" : str(origN), "hints" : [{"numberSystem" : "Sino-Korean"}]})

    return pool

# print(sinoKorean(12345))