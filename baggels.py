"""Bagels, by Al Sweigart al@inventwithpython.com
A deductive logic game where you must guess a number based on clues"""

import random

NUM_DIGITS = 3 # (!) Try setting this to 1 or 10.
MAX_GUESSSES = 10 # (!) Try Setting this to 1 or 100.


def main():
    print('''Bagels, a duductive logic game.
          By Al Sweigart al@inventwithpython.com
          
          I am thinking of a {}-digit number with no repeated digits.
          Try to guess what it is. Here are some clues:
          When I say:   That means:
            Pico        One digit is correct but in the wrong position.
            Fermi       One digit is correct and in the right position.
            Bagels      No digit is correct.)
          For Example, if the secret number was 248 and your geuss was 843, the 
          clues would be Fermi Pico.'''.format(NUM_DIGITS))
    while True: # Main game loop.
        #This stores the secret numbr the player needs to geuss:
        secretNum = getSecretNum()
        print('I have thought up a number.')
        print(' You have {} geusses to get it.'.format(MAX_GUESSSES))
        
        numGuesses = 1
        while numGuesses <= MAX_GUESSSES:
            guess = ''
            #Keep looping until they enter a valid guess:
            while len(guess) != NUM_DIGITS or not guess.isdecimal():
                print('Guess #{}: '.format(numGuesses))
                guess = input('> ')

            clues = getClues(guess, secretNum)
            print(clues)
            numGuesses += 1

            if guess == secretNum:
                break #They are correct, so break out of this loop.
            if numGuesses > MAX_GUESSSES:
                print('You ran out of guesses.')
                print('The answer was {}.'.format(secretNum))
    
        #Ask the player if the want to play again.
        print('Do you want to play again? (yes or no)')
        if not input('> ').lower().startswith('y'):
            break
    print('Thanks for playing!')

    def getSecretNum():
        """Returns a string made up of NUM_DIGITS unique random digits."""
        numbers = list('0123456789') # create a list of digits 0 to 9.
        random.shuffle(numbers) # Shuffle them into random order.

        #Get the first NUM_DIGITS in the list for the secret number:
        secretNum = ''
        for i in range(NUM_DIGITS):
            secretNum += str(numbers[i])
        return secretNum
    
    def getClues(guess, secretNum):
        """Returns a string with the pico, fermi, bagels clues for a guess 
        and secret number pair."""
        if guess == secretNum:
            return 'You got it!'
        
        clues = []

        for i in range(len(guess)):
            if guess[i] == secretNum[i]:
                # A correct digit is in the correct place.
                clues.append('Fermi')
            elif guess[i] in secretNum:
                # A correct digit is in the incorrect place.
                clues.append('Pico')
        if len(clues) == 0:
            return 'Bagels' # There are no correct digits at all.
        else:
            #Sort the clues into alphabetical order so their original order
            # doesn't give information away
            clues.sort()
            # Make a single string from the list of string clues.
            return ' '.join(clues)
        
    #If the program is (run instead of imported), run the game:
    if __name__ == '__main__':
        main()

