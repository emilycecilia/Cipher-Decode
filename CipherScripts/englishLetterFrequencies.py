# Frequency percentage of English letters, from Emory Oxford College Department of Mathematics and Computer Science

LETTER_FREQUENCY = {'A':0.0816, 'B':0.01492, 'C':0.02782, 'D':0.04253, 'E':0.12702, 'F':0.02228, 'G':0.02015, 
                'H':0.06094, 'I':0.06966, 'J':0.00153, 'K':0.00772, 'L':0.04025, 'M':0.02406, 'N':0.06749, 
                'O':0.07507, 'P':0.01929, 'Q':0.00095, 'R':0.05987, 'S':0.06327, 'T':0.09056, 'U':0.02758, 
                'V':0.00978, 'W':0.02360, 'X':0.00150, 'Y':0.01974, 'Z':0.00074}


# Create digram as 2d list so all elements can be accessed by indices
# Each slot holds dictionary mapping of letter pair to frequency
def textDigram(alphabetList):

    digramMatrix = []
    for first in alphabetList:
        row = []
        for second in alphabetList:
            alphaPair = str(first + second)
            dictPair = {alphaPair: 0}
            row.append(dictPair)
        digramMatrix.append(row)
    return digramMatrix


def dictPrettyPrint(dictionary):
    print("BEGIN PRINT\n")
    for row in dictionary:
        print(row)
    print("END PRINT\n")


def swapCipher(cipher, a, b):
    # Swap rows a and b 
    rowA = cipher[a]
    rowB = cipher[b]

    cipher[a] = rowB
    cipher[b] = rowA

    # Iterate through each row to swap elements at column index
    for row in cipher:
        colA = row[a]
        colB = row[b]

        row[a] = colB
        row[b] = colA

    dictPrettyPrint(cipher)

# Create digram of English letter frequency pairs #


def englishDigram(blankDigram):
    # Already calculated, just for more efficiency, can be dynamically calculated if preferred
    TOTAL_COUNT = 4324127906

    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphabetList = list(alphabet)
    alphaLen = 26

    digram = blankDigram

    # Define difference to convert ASCII values of characters to list indices 0-25
    conversionDiff = 65

    textFile = open("englishBigramFreq.txt", "r")
    for line in textFile:
        pair, count = line.split(" ")
        rowInd = ord(pair[0]) - conversionDiff
        colInd = ord(pair[1]) - conversionDiff
        
        # Replace current value in digram with correct frequency
        frequency = float(int(count) / TOTAL_COUNT)

        # If statement needed if alphabet is fewer than 26 letters
        if rowInd < alphaLen and colInd < alphaLen:
            digram[rowInd][colInd] = {pair: frequency}

        for row in digram:
            pairMapped = {pair: 0}
            if pairMapped in row:
                # pairMapped[pair] = float(int(count) / TOTAL_COUNT)
                # print(f"Found {pairMapped}, count should be {float(int(count) / TOTAL_COUNT)}")
                # # row[pair] = float(int(count) / TOTAL_COUNT)
                val = float(int(count) / TOTAL_COUNT)
                pairMapped = {pair: val}
                break

    print(digram)



# currentKey = list("JFYXTMNISWQBRZGHDKUALEPCOV")
# cipher = textDigram(currentKey)
# a = 0
# b = 3
# swapCipher(cipher, a, b)
# dictPrettyPrint(cipher)

# blankDigram = textDigram(currentKey)
# englishDigram(blankDigram)
