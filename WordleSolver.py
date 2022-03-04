import random
from collections import Counter

words = []
with open('wordle-nyt-answers-alphabetical.txt','r') as file:
    words = [line.strip() for line in file]
    
def guesser(guess, guesses, wordInfo, wordCount, answer, answerCount):
    if guesses != 1:
        print(f'Guess: {guess}')
    word = {}
    guessInfo = []
    for i, char in enumerate(guess):
        word[char] = word.get(char, 0) + 1
        if char == answer[i]:
            guessInfo.append([char, 2])
            # for j in range(0,i):
            #     if 
        #ANSWER: S A S S S
        #GUESS:  S S S S S
        #SHOULD: 2 0 2 2 2
        elif char in answer:
            if word.get(char) <= answerCount.get(char):
                guessInfo.append([char, 1])
            else:
                guessInfo.append([char, 0])
        else:
            guessInfo.append([char, 0])
    print(guessInfo)
    wordInfo.append(guessInfo)
    #print(Counter(wordInfo))
    for guessInfos in wordInfo:
        for i, info in enumerate(guessInfos):
            if info[1] == 2:
                wordCount[info[0]] = max(wordCount.get(info[0],0), guessInfos.count(info) + guessInfos.count([info[0], 1]))
            #if all(count == 0 and letter == info[0] for (letter, count) in info):
            if info[1] == 1:
                wordCount[info[0]] = max(wordCount.get(info[0],0), 1)
            if info[0] == 0:
                if info[0] not in wordCount:
                    wordCount[info[0]] = 0
    print(wordCount)
    if guess == answer:
        return guesses
    else:
        possibleWords = []
        for word in words:
            valid = True
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
                        
            if valid:
                possibleWords.append(word)
        return guesser(possibleWords[random.randint(0,len(possibleWords)-1)], guesses + 1, wordInfo, wordCount, answer, answerCount)

def getLetter(letters, letter):
        letter1 = {k: v[0] for k, v in sorted(letters.get(letter).items(), key=lambda item: item[1][0], reverse=True)}
        print(f'before {letter}:\n{letter1}')
        letter2 = {k: v[1] for k, v in sorted(letters.get(letter).items(), key=lambda item: item[1][1], reverse=True)}
        print(f'after {letter}:\n{letter2}')
        return

def main(efficiency, count):
    answer = words[random.randint(0,len(words)-1)]
    answerCount = {k : answer.count(k) for k in answer}
    print(answer)
    print(answerCount)
    guess = words[random.randint(0,len(words)-1)]
    guesses = guesser(guess, 1, [], {}, answer, answerCount)
    print(f'Took {guesses} guesses')
    efficiency.append(guesses)
    if count == 10:
        return efficiency
    return main(efficiency, count+1)

if __name__ == '__main__':
    efficiency = main([], 1)
    print(sum(efficiency) / len(efficiency))
