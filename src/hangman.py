import requests
import random

class Hangman():

    def __init__(self):
        self.word = None
        self.user_input = None
        self.incorrect_guess = []
        self.word_length = 0
        self.guesses = 0
        self.guessed_word = []
        self.correct_guess = []
        self.game_type = None

    def run_helper(self):
        print("""
        Hello, welcome to Hangman!
        Would you like to play 1 Player or 2 Player
        Type '1 Player' or '2 Player'
        """)
        self.game_type = input()

        if self.game_type == "1 Player":
            self.word = self.pull_word()


    def pull_word(self):
        word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
        response = requests.get(word_site)
        WORDS = response.content.splitlines()
        word = random.choice(WORDS)
        return word

if __name__ == '__main__':
    h = Hangman()
    h.run_helper()
