from englishLetterFrequencies import LETTER_FREQUENCY
from englishLetterFrequencies import textDigram
from englishLetterFrequencies import dictPrettyPrint as prettyPrint
import regex


# Emily Metzger 2022 #
# Adapted from A Fast Method for the Cryptanalysis of Substitution Ciphers, Thomas Jakobsen #
# A program to decrypt ciphertext encoded using a monoalphabetic cipher with the 26 English letters #


# Store frequency count of each letter in dictionary, returning text stripped of non-alphabetic characters #
def countLetters(text, frequencyCount):
    # Strip non-letter characters from encrypted text
    textStr = ""
    for char in text:
        if char.isalpha():
            textStr += char.upper()
            frequencyCount[char.upper()] += 1
    
    # Return stripped text
    return textStr


# Convert letter count values from integer count to frequency percentage and return new dictionary #
def countToFrequency(frequencyCount, numChars):
    # Create new dictionary for percentages
    frequencyPercent = {}

    # Iterate through keys of count dictionary and convert to percentages
    for key in frequencyCount:
        count = frequencyCount[key]

        # Cast result to float to store decimals
        frequencyPercent[key] = float(count/numChars)

    return frequencyPercent


# Map english letters to ciphertext values by frequencies $
def firstMapping(frequencyPercent, key):
    # Create list of key and dictionary to hold mappings as english:cipher
    cipherMappingDict = {}

    # Create dictionary copies to preserve originals
    freqCopy = dict(frequencyPercent)
    englishCopy = dict(LETTER_FREQUENCY)

    # Iterate through dictionary, mapping keys by frequency
    s = ""
    while freqCopy:
        # Get maximum frequency value of both dictionaries
        cipherMax = max(freqCopy, key=freqCopy.get)
        englishMax = max(englishCopy, key=englishCopy.get)

        # Remove max pairs from dictionaries
        freqCopy.pop(cipherMax)
        englishCopy.pop(englishMax)

        # Add maximum occurring letters to dictionary as a pair
        cipherMappingDict[englishMax] = cipherMax

        # Append cipher value to key
        key.append(cipherMax)

    # Restore frequency dictionary
    frequencyPercent = freqCopy
    
    # Return new mapping dictionary
    return cipherMappingDict


# Create digram of English letter frequency pairs #
def englishDigram(blankDigram):
    # Already calculated, just for more efficiency, can be dynamically calculated if preferred
    TOTAL_COUNT = 4324127906

    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphaLen = len(alphabet)

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

        # Check needed if alphabet is fewer than 26 letters
        if rowInd < alphaLen and colInd < alphaLen:
            digram[rowInd][colInd] = {pair: frequency}

    return digram


# Create digram of ciphertext letter frequency pairs #
def cipherDigram(digram, text, numChars):
    # Iterate through each row by element to get pair, check text for occurrence
    for row in digram:

        # Iterate through each dictionary in the row
        for i in range(0, 26):

            # Get key from dictionary to determine pair to look for
            key = list(row[i].keys())[0]

            # Use REGEX to count instances of letter pair
            num = len(regex.findall(key, text, overlapped=True))

            # Calculate frequency as a percent and store in map
            frequency = float(num / numChars)
            row[i] = {key:frequency}

    return(digram)


# Use summation method f(t) to calculate sum of differences between accurracy frequencies
def differenceSummation(englishDigram, cipherDigram):
    # Iterate through both matricies
    rowInd = 0
    colInd = 0
    differenceSum = 0

    for row in cipherDigram:
        colInd = 0
        for col in row:
            key = list(col.keys())[0]
            englishKey = list(englishDigram[rowInd][colInd].keys())[0]
            difference = cipherDigram[rowInd][colInd][key] - englishDigram[rowInd][colInd][englishKey]
            differenceSum += abs(difference)
            colInd += 1
        rowInd += 1

    return differenceSum


# Swap rows and columns according to optimization algorithm
def swapCipherDigram(cipher, indA, indB):
    digram = list(cipher)
    # print(indA)
    # print(indB)
    # Swap rows a and b
    rowA = digram[indA]
    rowB = digram[indB]
    # print(f"A: {rowA}\nB:{rowB}")

    digram[indA] = rowB
    digram[indB] = rowA
    # print(f"A: {digram[indA]}\nB:{digram[indB]}")

    # Iterate through each row to swap elements at column index
    for row in digram:
        colA = row[indA]
        colB = row[indB]
        # print(f"Elements: a = {colA}, b = {colB}")

        row[indA] = colB
        row[indB] = colA
        # print(f"Switched: a = {row[indA]}, b = {row[indB]}")

    # print(f"Ind A = {indA}, Ind B = {indB}\nRow A = {rowA}\nrowB = {rowB}\nValue A = {colA}, ValueB = {colB}")
    
    return digram


# Run decryption 
def main():
    text = "YMTRU XTSMF XFQNG WFWDF SIFXY FYZJT SYMJT AFQGZ YINID TZWJF QNEJM NXRTY MJWMF XFGZN QINSL TKMJW TBSYM JSFRJ BFXXJ QJHYJ IFGTZ YJQJA JSIJH FIJXF LTGDY MJKNW XYUJT UQJBM TRTAJ INSNY BFXYM JKNWX YBTRJ SXITW RFYTX ZFSIY MJFWH MNYJH YBFXF GZHPJ DJMJW XJQKS TBYJQ QRJUQ JFXJB MFYNX NYXFI IWJXX SZRGJ W"

    # Initialize container variables and alphabet string
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphabetList = list(alphabet)

    mapping = {}
    frequencyCount = {}
    for key in alphabetList:
        mapping[key] = ""
        frequencyCount[key] = 0

    # Strip text and count letter occurrences 
    textStr = countLetters(text, frequencyCount)

    # Store total number of letters in cipher text
    numChars = len(textStr)

    # Calculate map with frequency percentages
    frequencyPercent = countToFrequency(frequencyCount, numChars)

    # Create an initial mapping of letters strictly by frequencies and a starting key
    firstKey = []
    pairMappings = firstMapping(frequencyPercent, firstKey)

    english = englishDigram(textDigram(alphabetList))
    firstKey = alphabetList
    # Fill in digram of cipher pair frequencies
    cipher = cipherDigram(textDigram(firstKey), textStr, numChars)

    # Define variables
    alphaLength = len(alphabet)
    a = b = 1
    iterCount = 0
    currentKey = firstKey

    # Calculate initial correctness
    difference = differenceSummation(english, cipher)

    # while (b < alphaLength):
    while(b < alphaLength):
        # Create a new key to check
        newKey = list(currentKey)

        # Swap a and b in new key
        valueA = newKey[a - 1]
        valueB = newKey[a + b - 1]
        newKey[a - 1] = valueB
        newKey[a + b - 1] = valueA

        a += 1

        # Swap cipher key if a and b are in range, otherwise move to next row
        if (a + b <= alphaLength):
            swappedCipher = swapCipherDigram(cipher, (a-2), (b-2))
        else:
            a = 1
            b += 1
            swappedCipher = swapCipherDigram(cipher, (a-2), (b-2))
            
        newDifference = differenceSummation(english, swappedCipher)

        # Only update values to new ones if difference in frequencies have improved
        if newDifference < difference:
            difference = newDifference
            currentKey = newKey
            cipher = swappedCipher
            a = b = 1

        iterCount += 1
        if iterCount % 100 == 0:
            print(f"{iterCount} iterations completed. Current key is: {currentKey}")

        if iterCount >= 1000:
            break

        # ####### DEBUG #######

        # values = f"Iteration {iterCount}\nOriginal key:\t{firstKey}\nCurrent key:\t{currentKey}\na = {a}, b = {b}\nCurrent difference is {newDifference}, best difference is {difference}"
        # print(values)

        # textIn = input("Press 'x' to exit, press any other key to continue: ")
        # if textIn == "x" or textIn == "clear":
        #     break

        # ##### END DEBUG #####


    print(f"Exited program after {iterCount} iterations. Best found key is: \n\t\t{currentKey}")
            

if __name__ == "__main__":
    main()