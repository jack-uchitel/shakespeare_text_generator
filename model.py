import spacy
import random
import hf
import statistics


class Model:
    def __init__(self, corpus, order, pos=False, split=.2):
        self.corpus = corpus
        self.order = order
        self.pos = pos
        with open(self.corpus, 'r') as file:
            self.text = file.read()
        self.tokens = self.tokenizeWords()
        self.markovSplice, self.trainingSplice = hf.spliceArray(self.tokens, split)
        self.posTransitions = hf.train(self.makePOSTransitions()) if self.pos else None
        self.transitions = hf.train(self.makeMarkov(self.tokens)) if not self.pos else hf.train(self.makeMarkov(self.markovSplice))

    def tokenizeWords(self, entry=None):
        nlp = spacy.load("en_core_web_sm")
        nlp.max_length = 5000000
        if entry is None:
            doc = nlp(self.text[:1000000])
        else:
            doc = nlp(entry)
        return [(token.text, token.pos_) for token in doc]

    def makePOSTransitions(self):
        posDict = {}
        for token in self.tokens:
            if token[1] not in posDict:
                posDict[token[1]] = [token[0]]
            else:
                posDict[token[1]].append(token[0])
        return posDict

    def makeMarkov(self, tokens):
        markovDict = {}
        for i in range(len(tokens) - self.order):
            markovEntry = ' '.join([token[self.pos] for token in tokens[i:i + self.order]])
            if markovEntry not in markovDict:
                markovDict[markovEntry] = [tokens[i + self.order][self.pos]]
            else:
                markovDict[markovEntry].append(tokens[i + self.order][self.pos])
        return markovDict

    def generate(self, startWord, wordCount):
        print('Generating Shakespeare for you! This may take a minute...')
        output = self.tokenizeWords(startWord)
        words = self.order
        keyword = ' '.join(token[self.pos] for token in output)
        if len(output) != words:
            return 'Make sure to match the order!'
        while words < wordCount:
            selectorOne = random.random()
            selectorTwo = random.random()
            for value in self.transitions[keyword]:
                if value[1] < selectorOne <= value[2]:
                    if self.pos:
                        word = ''
                        pos = value[0]
                        for item in self.posTransitions[value[0]]:
                            if item[1] < selectorTwo < item[2]:
                                word = item[0]
                    else:
                        word = value[0]
                        pos = None
                    output.append((word, pos))
                    keyword = ' '.join(token[self.pos] for token in output[-self.order:])
                    words += 1
        return hf.cleanText(' '.join(pair[0] for pair in output))

    def compare(self, inputArray):
        probability = 0.0
        totalItems = len(inputArray)
        previousWord = inputArray[0]
        for word in inputArray[1:]:
            if previousWord in self.transitions:
                for entry in self.transitions[previousWord]:
                    if entry[0] == word:
                        probability += (entry[2] - entry[1])
                        previousWord = word
                        break
        return probability/totalItems

    def estimate(self):
        trainingArray = self.trainingSplice
        trainingValues = []
        i = 0
        while i < len(trainingArray) - 10:
            testInput = [item[0] for item in trainingArray[i:i+10]]
            trainingValues.append(self.compare(testInput))
            i += 10
        mean = statistics.mean(trainingValues)
        std = statistics.stdev(trainingValues)
        while True:
            inputString = input("Write your sentence, or press enter to quit: ")
            if inputString == '':
                break
            inputArray = [token[0] for token in self.tokenizeWords(inputString)]
            inputProb = self.compare(inputArray)
            print(mean, std, inputProb, (inputProb - mean)/std)



