from collections import Counter
import copy
import random
import time
    
def guesser(guess, guesses, wordInfo, wordCount, answer, answerCount):
    print(f'Guess: {guess}')
    #have we found the answer
    if guess == answer:
        return guesses
    #assign colors to your guess (0=gray, 1=yellow, 2=green)
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
    #accumulate all info we have on letter data (number of each letter known, and certainty of the number known)
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
    #preset next guess if we get all gray letters for the guess crane to save run time
    if all(item[1] == 0 for item in guessInfo) and guesses==1:
        possibleWords = ['lousy']
    #find list of possible answers given the data we have
    else:
        possibleWords = []
        for word in words:
            valid = True
            #compare possible word with the character requirements we have
            wordCounter = Counter(word)
            for letter in wordCount:
                if wordCount.get(letter)[0] == 0:
                    if letter in wordCounter:
                        valid = False
                else:
                    if letter not in wordCounter:
                        valid = False
                    else:
                        if wordCount.get(letter)[1]:
                            if wordCount.get(letter)[0] != wordCounter.get(letter):
                                valid = False
                        elif wordCount.get(letter)[0] > wordCounter.get(letter):
                            valid = False   
                if not valid:
                    break
            #compare possible word with info we have about our current guess
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
                possibleWords.append(word)
    #check each possible guess against each possible answer to see which eliminates the most options for future answers
    wordDict = {}
    for word in possibleWords:
        for word2 in possibleWords:
            if word in wordDict:
                wordDict[word] += tester(word, copy.deepcopy(possibleWords), 1, copy.deepcopy(wordInfo), copy.deepcopy(wordCount), word2, {k : word2.count(k) for k in word2})
            else:
                wordDict[word] = 1
    wordDict = {k: v for k, v in sorted(wordDict.items(), key = lambda item:item[1])}
    print(f'Guess choices: {wordDict}')
    return guesser(list(wordDict.keys())[0], guesses + 1, wordInfo, wordCount, answer, answerCount)

def tester(guess2, possibleWords2, guesses2, wordInfo2, wordCount2, answer2, answerCount2):
    #have we found the answer
    if guess2 == answer2:
        return guesses2
    #assign colors to your guess (0=gray, 1=yellow, 2=green)
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
    #accumulate all info we have on letter data (number of each letter known, and certainty of the number known)
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
    #find list of possible answers given the data we have
    words = copy.deepcopy(possibleWords2)
    possibleWords2 = []
    for word in words:
        valid = True
        #compare possible word with the character requirements we have
        wordCounter = Counter(word)
        for letter in wordCount2:
            if wordCount2.get(letter)[0] == 0:
                if letter in wordCounter:
                    valid = False
            else:
                if letter not in wordCounter:
                    valid = False
                else:
                    if wordCount2.get(letter)[1]:
                        if wordCount2.get(letter)[0] != wordCounter.get(letter):
                            valid = False
                    elif wordCount2.get(letter)[0] > wordCounter.get(letter):
                        valid = False 
            if not valid:
                break   
        #compare possible word with info we have about our current guess     
        for guessInfos in wordInfo2:  
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
            possibleWords2.append(word)
    return len(possibleWords2)

def main(efficiency, count):
    guess = 'crane'
    for count, answer in enumerate(words):
        answerCount = {k : answer.count(k) for k in answer}
        print(f'Solving for {answer}')
        guesses = guesser(guess, 1, [], {}, answer, answerCount)
        efficiency.append(guesses)
        print(f'\n{answer} took {guesses} guesses')
        print(f'Count: {count+1}')
        print(f'Time: {time.perf_counter() - start}')
        print(f'Avg Count: {sum(efficiency) / (count+1)}')
        print(f'Avg Time: {(time.perf_counter() - start)/(count+1)}\n')
    return efficiency

if __name__ == '__main__':
    with open('wordle-nyt-answers-alphabetical.txt','r') as file:
        words = [line.strip() for line in file]
    random.shuffle(words)
    start = time.perf_counter()
    efficiency = main([], 1538)
    print(sum(efficiency) / len(efficiency))
    print('Done')
