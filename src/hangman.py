import requests
import random as r
import re


class Hangman():

    def __init__(self):
        self.word = None
        self.user_guess = None
        self.hidden_word = []
        self.guessed_letters = []
        self.incorrect_guesses = []
        self.game_type = None
        self.game_continue = True
        self.alphabet = list(map(chr, range(65, 90)))
        self.reg_pattern = r"b'(\w+)'"

    def run_helper(self):
        print("""
        Hello, welcome to Hangman!
        Would you like to play 1 Player or 2 Player
        Type '1 Player' or '2 Player'
        """)
        self.game_type = input().lower().strip()

        if self.game_type == "1 player":
            self.word, self.hidden_word = self.pull_word()
        elif self.game_type == "2 player":
            self.word, self.hidden_word = self.input_word()
        else:
            exit()

        print(self.hidden_word)

        self.user_guess = self.make_guess()
        self.hidden_word = self.solved_letters(self.word,
                                               self.user_guess,
                                               self.hidden_word)

        while self.game_continue and len(self.incorrect_guesses) < 6:
            print(self.hidden_word)
            print("Guessed letters: " + str(self.guessed_letters))

            print(f"""
            Do you want to guess another letter or guess the word?
            Incorrect guesses left: {str(6 - len(self.incorrect_guesses))}

            Type 'letter' for guessing another letter
            Type 'word' for guessing the word
            """)

            user_input = input().lower()

            if user_input == 'letter':
                self.user_guess = self.make_guess()
                self.hidden_word = self.solved_letters(self.word,
                                                       self.user_guess,
                                                       self.hidden_word)
            elif user_input == 'word':
                self.solve_word(self.word)
            else:
                print("Please type 'letter' or 'word' to continue.")

            if '_' not in self.hidden_word:
                print("You Win!")
                print(f"The word was {self.word}")
                self.game_continue = False

        if len(self.incorrect_guesses) == 6:
            print("The correct word was:")
            print(self.word)
            print('Sorry, you lose!')

    def pull_word(self):
        word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
        response = requests.get(word_site)
        WORDS = response.content.splitlines()
        word = str(r.choice(WORDS).upper())
        word = re.findall(self.reg_pattern, word)[0]
        hidden_word = ['_']*len(word)
        return word, hidden_word

    def input_word(self):
        if r.randint(0, 100) <= 50:
            print('Player 1, please input a word!')
        else:
            print('Player 2, please input a word!')
        word = input().upper()
        hidden_word = ['_']*len(word)
        return word, hidden_word

    def make_guess(self):
        print("Please guess a letter.")
        self.user_guess = input().upper()

        if self.user_guess not in self.alphabet:
            print("Please submit a valid character.")
            self.user_guess = input().upper()

        self.guessed_letters.append(self.user_guess)

        return self.user_guess

    def solved_letters(self, word, guess, hidden_word):
        if guess in word:
            positions = [pos for pos, char in enumerate(word) if char == guess]
            for i in positions:
                hidden_word[i] = guess
        else:
            self.incorrect_guesses.append(guess)

        return hidden_word

    def solve_word(self, word):
        print("Take a guess at the word!")
        word_guess = input().upper()

        if word_guess == word:
            print("You Win!")
            print(f"The word was {word}")
        else:
            print("Sorry, you lose!")

        self.game_continue = False

        return None


if __name__ == '__main__':
    h = Hangman()
    h.run_helper()

    print("Would you like to play again? (yes / no)")
    play_again = input().lower()

    while play_again == 'yes':
        h = Hangman()
        h.run_helper()

        print("Would you like to play again? (yes / no)")
        play_again = input().lower()

    print('See you next time!')
