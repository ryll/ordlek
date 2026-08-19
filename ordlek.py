from random import choice

saol = []

with open("SAOL_14_clean.txt", encoding="UTF-8") as f:
    for line in f:
        saol.append(line.rstrip())

def playLoop(saol):
    letters = int(input("Hur många bokstäver? (3-20)"))
    words = [word for word in saol if len(word) == letters]
    guessed = []
    correct = ['_']*letters
    answer = choice(words)

    while True:
        print()
        print(" ".join(correct))
        print("Gissade ord:"," ".join(guessed))
        
        while True:
            guess = input("Gissa på ett ord: ")
            if guess in words:
                words.remove(guess)
                break
            elif guess not in saol:
                print("Ordet finns inte i SAOL, försök igen.")
                continue
            else:
                print("Inte ett accepterat ord, försök igen.")
                continue
        
        guessed.append(guess)
        if guess == answer:
            print("Rätt!")
            break

        for i in range(letters):
            tempWords = words[:]
            if answer[i] == guess[i]:
                correct[i] = guess[i]
                for word in words:
                    if word[i] != guess[i]:
                        tempWords.remove(word)
            words = tempWords[:]

if __name__ == "__main__":
    playLoop(saol)
