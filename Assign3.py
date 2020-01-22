def compress(fname):
    inFile = open(fname, "r")
    outFileName = fname.replace(".txt", ".enc")
    outFile = open(outFileName, "w")
    #line = next(inFile)
    for line in inFile:
        line = line.strip()
        sortedFreqList = getSortedFreq(line)
        finalDict = getBinaryDict(sortedFreqList)
        print(finalDict, file = outFile)
        compressedBinarySring = ""
        for letter in line:
            compressedBinarySring = compressedBinarySring + finalDict[letter]
        print(compressedBinarySring, file = outFile)
    return (compressedBinarySring, finalDict)

def uncompress(fname):
    inFile = open(fname, "r")
    dictString = next(inFile)
    binaryString = next(inFile)
    dictionaryOld = eval(dictString)
    newDict =  dict([(value, key) for key, value in dictionaryOld.items()])
    print(newDict)
    currentBinString = ""
    finalWord = ""
    for letter in binaryString:
        currentBinString = currentBinString + letter
        if(currentBinString in newDict.keys()):
            
            finalWord = finalWord + newDict[currentBinString]
            currentBinString = ""

    return finalWord

def analyze(fname):
    inFile = open(fname)
    line = next(inFile)
    line = line.strip()
    uncompressedLength = len(line) * 8
    print("length of uncompressed string is ", uncompressedLength)
    numChar = count(line)
    bitsNeeded = bits(numChar)
    smallestFixLength = len(line) * bitsNeeded
    print("Length of uncompressed string using the smallest fixed-length bit-pattern (",bitsNeeded," bits) ", smallestFixLength)
    compressedString, finalDict = compress(fname)
    compressedStringLen = len(compressedString)
    noDictRatio = compressedStringLen/smallestFixLength
    dictBits = 0
    for key in finalDict:
        dictBits = dictBits + 8
        dictBits = dictBits + len(finalDict[key])
    dictRatio = (compressedStringLen + dictBits)/smallestFixLength
    print("Length of compressed binary string is ", compressedStringLen)
    print("Compression ratio without dictionary is ", noDictRatio)
    print("Compression ratio with dictionary is ", dictRatio)
    
def frequency(line):
    compressDic = {}
    line = line.strip()
    for i in line:
        if i in compressDic:
            compressDic[i] += 1
        else:
            compressDic[i] = 1

    return compressDic


def getSortedFreq(line):
    freqDic = frequency(line)
    freqList = dic2list(freqDic)
    sortedFreqList = insertSorted(freqList)

    return sortedFreqList

def dic2list(dictionary):
    lst = []
    for key in dictionary:
        lst.append((key, dictionary[key]))
    return lst

def insertSorted(lst):
    return sorted(lst, key=lambda x: x[1])
    #return sorted(dic, key=dic.__getitem__)

def getBinaryDict(myList):
    finalDict = {}
    for item in myList:
        finalDict[item[0]] = ""
    while(len(myList)!= 1):
        item1 = myList.pop(0)
        item2 = myList.pop(0)
        newItem = (item1[0] + item2[0], item1[1] + item2[1])
        for letter1 in item1[0]:
            
            finalDict[letter1] = "0" + finalDict[letter1]
        for letter2 in item2[0]:
            finalDict[letter2] = "1" + finalDict[letter2]
        myList.append(newItem)
        myList = insertSorted(myList)

    return finalDict

def count(line):
    lst = []
    for i in line:
        if i not in lst:
            lst.append(i)
    return len(lst)

def bits(num):
    bits = 0
    while(2**bits < num):
        bits += bits + 1
    return bits
