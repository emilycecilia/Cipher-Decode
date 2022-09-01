from englishLetterFrequencies import textDigram

# Already calculated, just for more efficiency, can be dynamically calculated if preferred
TOTAL_COUNT = 4324127906

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alphabetList = []
alphabetList[:0] = alphabet

digram = textDigram(alphabetList)

textFile = open("englishBigramFreq.txt", "r")
for line in textFile:
    pair, count = line.split(" ")
    for row in digram:
        if pair in row:
            row[pair] = float(int(count) / TOTAL_COUNT)
            break

textFile.close()


