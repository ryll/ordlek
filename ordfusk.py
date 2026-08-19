from operator import itemgetter
from random import choice
from string import ascii_lowercase

alphabet = ascii_lowercase + "åäö"


def load_words(path="SAOL_14_clean.txt"):
    with open(path, encoding="UTF-8") as f:
        return [line.rstrip() for line in f]


def wordsort(words, letters):
    """
    Score each word by how far its letters deviate from the midpoint of
    positional frequency, then sort ascending. Favours words whose letters
    split the candidate set most evenly.
    """
    lst = [[word, 0] for word in words]
    letterCount = [{x: 0 for x in alphabet} for _ in range(letters)]

    # Count occurences of letters at every position
    for word, value in lst:
        for i, valDict in enumerate(letterCount):
            valDict[word[i]] += 1

    for i, (word, value) in enumerate(lst):
        lst[i][1] += round(sum(((letterCount[n][word[n]]-len(lst)/2)/len(lst))**2 for n in range(letters))**0.5, 4)
    return sorted(lst, key=itemgetter(1), reverse=False)


def wordsort2(words, letters):
    """
    Score each word by the mean positional frequency of its letters, then sort
    descending. Favours words built from the most common letters.
    """
    lst = [[word, 0] for word in words]
    letterCount = [{x: 0 for x in alphabet} for _ in range(letters)]

    # Count occurences of letters at every position
    for word, value in lst:
        for i, valDict in enumerate(letterCount):
            valDict[word[i]] += 1

    for i, (word, value) in enumerate(lst):
        lst[i][1] += round(sum(letterCount[n][word[n]]/len(lst) for n in range(letters))/letters, 4)
    return sorted(lst, key=itemgetter(1), reverse=True)


def main():
    saol = load_words()

    letters = int(input("How many letters? "))
    words = [word for word in saol if len(word) == letters]
    if not words:
        print("No words of that length in the word list.")
        return

    answer = choice(words)
    guessed = [set() for _ in range(letters)]
    correct = ['_']*letters
    print()
    print(len(words), "candidates")

    while True:
        print(" ".join(correct))
        print([wordsort(words, letters)[n] for n in range(min(5, len(words)))])
        print([wordsort2(words, letters)[n] for n in range(min(5, len(words)))])

        # Get guess
        while True:
            guess = input("Make a guess: ")
            if guess in words:
                words.remove(guess)
                break
            else:
                print("Not a valid word, try again")
                continue

        if guess == answer:
            print("Correct! The word was", answer)
            break

        for i in range(letters):
            guessed[i].add(guess[i])
            tempWords = words[:]
            if answer[i] == guess[i]:
                correct[i] = guess[i]
                for word in words:
                    if word[i] != guess[i]:
                        tempWords.remove(word)
            else:
                for word in words:
                    if word[i] == guess[i]:
                        tempWords.remove(word)
            words = tempWords[:]
        print(len(words), "candidates")
        if '_' not in correct:
            print("The word was", answer)
            break


if __name__ == "__main__":
    main()
