import random
import copy
from collections import Counter

words = []
with open('wordle-nyt-answers-alphabetical.txt','r') as file:
    words = [line.strip() for line in file]
    
def guesser(guess, guesses, wordInfo, wordCount, answer, answerCount):
    print(f'Guess: {guess}')
    word = {}
    guessInfo = []
    lettersNeeded = copy.deepcopy(answerCount)
    for i, char in enumerate(guess):
        if char == answer[i]:
            guessInfo.append([char, 2])
            lettersNeeded[char] -= 1
        else:
            guessInfo.append([char, 0])
    for i, char in enumerate(guess):
        if char in answer and guessInfo[i][1] != 2 and lettersNeeded[char] > 0:
            guessInfo[i] = [char, 1]
            lettersNeeded[char] -= 1
    # print(f'guess info: {guessInfo}')
    # print(f'letters needed: {lettersNeeded}')
    wordInfo.append(guessInfo)
    for guessInfos in wordInfo:
        for i, info in enumerate(guessInfos):
            if info[1] == 2:
                wordCount[info[0]] = [max(wordCount.get(info[0],[0,0])[0], guessInfos.count(info) + guessInfos.count([info[0], 1])),0 if [info[0],0] not in guessInfos else 1]
            if info[1] == 1:
                wordCount[info[0]] = [max(wordCount.get(info[0],[0,0])[0], guessInfos.count([info[0], 1])),0 if [info[0],0] not in guessInfos else 1]
            if info[1] == 0:
                if info[0] not in wordCount:
                    wordCount[info[0]] = [0,1]
    if guess == answer:
        return guesses
    else:
        possibleWords = []
        for word in words:
            valid = True
            for letter in wordCount:
                if wordCount.get(letter)[0] == 0:
                    if letter in Counter(word):
                        valid = False
                else:
                    if letter not in Counter(word):
                        valid = False
                    else:
                        if wordCount.get(letter)[1]:
                            if wordCount.get(letter)[0] != Counter(word).get(letter):
                                valid = False
                        elif wordCount.get(letter)[0] > Counter(word).get(letter):
                            valid = False   
                if not valid:
                    break   
            for guessInfos in wordInfo:
                for i, info in enumerate(guessInfos):
                    if info[1] == 2:
                        if word[i] != info[0]:
                            valid = False
                    elif info[1] == 1:
                        if word[i] == info[0]:
                            valid = False
                        if info[0] not in word:
                            valid = False
                    else:
                        if word[i] == info[0]:
                            valid = False
                    if not valid:
                        break          
            if valid:            
                possibleWords.append([word, 0])
        print(f'possible words first: {possibleWords}')
        print(f'word count: {wordCount}')
        possibleWordsCopy = copy.deepcopy(possibleWords)
        testerDict = {}
        for i, word in enumerate(possibleWords):
            print(f'word processing: {word[0]}')
            for j, word2 in enumerate(possibleWords):
                size = tester(word[0], possibleWordsCopy, 1, copy.deepcopy(wordInfo), copy.deepcopy(wordCount), word2[0], {k : word2[0].count(k) for k in word2[0]})
                #print(f'if you guess {word[0]} when the answer is {word2[0]} there are {size} possible valid answers')
                #print(f'so we assign {size} to {word[0]}')
                if word[0] in testerDict:
                    #print(f'adding {size} to {testerDict[word[0]]} at {word[0]} for answer {word2[0]}')
                    testerDict[word[0]] += size
                else:
                    #print(f'first size: {0} for {word[0]}')
                    testerDict[word[0]] = 0
                # input('continue?')
            print(f'word done {word[0]} with size {testerDict[word[0]]}')
        testerDict = {k: v for k, v in sorted(testerDict.items(), key = lambda item:item[1])}
        print(f'tester dict: {testerDict}')
        # possibleWords = sorted(possibleWords, key = lambda x:x[1])
        # print(possibleWords)
        return guesser(list(testerDict.keys())[0], guesses + 1, wordInfo, wordCount, answer, answerCount)
        # return guesser(possibleWords[0][0], guesses + 1, wordInfo, wordCount, answer, answerCount)

def tester(guess2, possibleWords2, guesses2, wordInfo2, wordCount2, answer2, answerCount2):
    guessInfo = []
    lettersNeeded = copy.deepcopy(answerCount2)
    for i, char in enumerate(guess2):
        if char == answer2[i]:
            guessInfo.append([char, 2])
            lettersNeeded[char] -= 1
        else:
            guessInfo.append([char, 0])
    for i, char in enumerate(guess2):
        if char in answer2 and guessInfo[i][1] != 2 and lettersNeeded[char] > 0:
            guessInfo[i] = [char, 1]
            lettersNeeded[char] -= 1
    wordInfo2.append(guessInfo)
    for guessInfos in wordInfo2:
        for i, info in enumerate(guessInfos):
            if info[1] == 2:
                wordCount2[info[0]] = [max(wordCount2.get(info[0],[0,0])[0], guessInfos.count(info) + guessInfos.count([info[0], 1])),0 if [info[0],0] not in guessInfos else 1]
            if info[1] == 1:
                wordCount2[info[0]] = [max(wordCount2.get(info[0],[0,0])[0], guessInfos.count([info[0], 1])),0 if [info[0],0] not in guessInfos else 1]
            if info[1] == 0:
                if info[0] not in wordCount2:
                    wordCount2[info[0]] = [0,1]
    if guess2 == answer2:
        return guesses2
    else:
        words = copy.deepcopy(possibleWords2)
        possibleWords2 = []
        for word in words:
            word = word[0]
            valid = True
            wordCounter = Counter(word)
            # print(f'guess: {guess2}')
            # print(f'answer: {answer2}')
            #print(f'valid word: {word}')
            # print(f'wordcounter: {wordCounter}')
            # print(f'wordcount2: {wordCount2}')
            # print(f'wordinfo2: {wordInfo2}')
            for letter in wordCount2:
                #print(f'letter: {letter}')
                if wordCount2.get(letter)[0] == 0:
                    if letter in wordCounter:
                        #print('1')
                        valid = False
                else:
                    if letter not in wordCounter:
                        #print('2')
                        valid = False
                    else:
                        if wordCount2.get(letter)[1]:
                            if wordCount2.get(letter)[0] != wordCounter.get(letter):
                                #print('3')
                                valid = False
                        elif wordCount2.get(letter)[0] > wordCounter.get(letter):
                            #print('4')
                            valid = False 
                if not valid:
                    break        
            for guessInfos in wordInfo2:  
                for i, info in enumerate(guessInfos):
                    if info[1] == 2:
                        if word[i] != info[0]:
                            #print('5')
                            valid = False
                    elif info[1] == 1:
                        if word[i] == info[0]:
                            #print('6')
                            valid = False
                        if info[0] not in word:
                            #print('7')
                            valid = False
                    elif word[i] == info[0]:
                        #print('8')
                        valid = False 
                    if not valid:
                        break    
            if valid:            
                possibleWords2.append(word)
            #else:
                #print('not valid')
    #print(f'test possible words 2: {possibleWords2}')
    return len(possibleWords2)


def main(efficiency, count):
    answer = words[random.randint(0,len(words)-1)]
    answerCount = {k : answer.count(k) for k in answer}
    print(answer)
    print(answerCount)
    guess = words[random.randint(0,len(words)-1)]
    guess = 'crane'
    guesses = guesser(guess, 1, [], {}, answer, answerCount)
    print(f'Took {guesses} guesses')
    efficiency.append(guesses)
    if count == 100:
        return efficiency
    print(count)
    print(sum(efficiency) / len(efficiency))
    return main(efficiency, count+1)

if __name__ == '__main__':
    efficiency = main([], 1)
    print(sum(efficiency) / len(efficiency))
    print('Done')
