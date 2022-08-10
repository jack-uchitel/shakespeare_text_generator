import random
import math

def cleanText(text):
    cleanedText = text
    for item in [' .', ' !', ' ?', ' ,', ' :', ' ;', " '"]:
        cleanedText = cleanedText.replace(item, item[1])
    cleanedText = cleanedText.replace("' ", "")
    return cleanedText


def train(dictionary):
    transitions = {}
    for key in dictionary:
        transitions[key] = []
        values = {}
        numItems = len(dictionary[key])
        probability = 0.0
        for value in dictionary[key]:
            if value not in values:
                values[value] = 1
            else:
                values[value] += 1
        for pair in values:
            transitions[key].append((pair, probability, probability + (values[pair] / numItems)))
            probability += (values[pair] / numItems)
    return transitions


def spliceArray(array, portion):
    totalEntries = len(array)
    startingIndex = math.floor(min(random.random(), 1 - portion) * totalEntries)
    endingIndex = startingIndex + math.floor(totalEntries * portion)
    bigSplice = array[0:startingIndex] + array[endingIndex:]
    smallSplice = array[startingIndex:endingIndex]
    return bigSplice, smallSplice




