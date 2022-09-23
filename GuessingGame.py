
import nltk
import sys
import random

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

#nltk.download('stopwords')
#nltk.download('wordnet')
#nltk.download('omw-1.4')
#nltk.download('averaged_perceptron_tagger')


def processText(text):
    lemmatizer = WordNetLemmatizer()
    tokens = [token for token in text if token.isalpha() and token not in stopwords.words('english') and len(token) > 5]

    lemmas = set([lemmatizer.lemmatize(token) for token in tokens])
    pos = pos_tag(lemmas)
    print("First 20 POS tags: ", pos[:20])

    nouns = [token[0] for token in pos if token[1][0] == "N"]
    print("Number of tokens: ", len(tokens))
    print("Number of nouns: ", len(nouns))
    return tokens, nouns


def printHidden(word):
    result = ""
    for w in word:
        result += w + " "
    print(result[:-1])


def game(words, score=5, won=False):
    # Define the words that will be used in the game
    randomWord = random.choice(words)  # Kept as a string for easy printing
    key = [*randomWord]  # a list to check the full word against
    word = [*randomWord]  # the word to be guessed
    hiddenWord = ['_'] * len(word)  # the blanks that will be filled in

    print("Guess the hidden word! Your current score is: ", score)
    printHidden(hiddenWord)
    guess = input("Guess a letter: ")
    won = False
    while score > 0 and guess != '!':
        if guess in word:
            hiddenWord[word.index(guess)] = guess
            word[word.index(guess)] = "_"
            score += 1
            print("Correct! Your score is:", score)
        else:
            score -= 1
            print("Wrong! Your score is:", score)
        printHidden(hiddenWord)
        if hiddenWord == key:
            won = True
            break
        guess = input("Guess a letter: ")

    if guess == '!':
        sys.exit(0)
    if won:
        print("You found the word! Your score is:", score)
    else:
        print("You Lose!")
        print("The word was:", randomWord)
    if input("Play again? (y/n): ") == 'y':
        game(words)


def main():
    if len(sys.argv) != 2:
        sys.exit("Error: incorrect arguments")

    infile = open(sys.argv[1], 'r')
    tokens = []
    for line in infile:
        tokens.extend([x.lower() for x in line.split()])

    tokenSet = set(tokens)
    print("Lexical diversity: %.2f" % (len(tokenSet)/len(tokens)))

    tokens, nouns = processText(tokens)

    count = {}
    for noun in nouns:
        if count.get(noun):
            count[noun] += 1
        else:
            count[noun] = 1

    gameList = [x[0] for x in sorted(count.items(), key=lambda item: item[1])][-50:]
    print("The 50 most common words are: ", gameList)
    game(gameList)


if __name__ == '__main__':
    main()













