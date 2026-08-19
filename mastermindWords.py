from random import choice

saol = []

with open("SAOL_14_clean.txt", encoding="UTF-8") as f:
    for line in f:
        saol.append(line.rstrip())

def playLoop(saol):
    letters = int(input("Hur många bokstäver? (3-20): "))
    words = [word for word in saol if len(word) == letters]
    guessed = []
    answer = choice(words).upper()
    
    while True:        
        while True:
            guess = input("Gissa på ett ord: ")
            if guess in words:
                guess = guess.upper()
                break
            elif guess not in saol:
                print("Ordet finns inte i SAOL, försök igen.")
                continue
            else:
                print("Inte ett accepterat ord, försök igen.")
                continue
        
        if guess == answer:
            print("Rätt!")
            break
        ansList = list(answer)
        guessList = list(guess)
        X,O = 0,0
        for i in range(letters):
            if answer[i] == guess[i]:
                ansList[i],guessList[i] = "-","-"
                X += 1
        ansList = list(filter(lambda x: x != "-",ansList))
        guessList = list(filter(lambda x: x != "-",guessList))
        
        for letter in guessList:
            if letter in ansList:
                ansList.remove(letter)
                O += 1
        
        guessed.append([guess," ".join("X"*X + "O"*O + "_"*(letters-X-O))])
        print("\n")
        for guess,result in guessed:
            print(guess,result)

if __name__ == "__main__":
    playLoop(saol)
