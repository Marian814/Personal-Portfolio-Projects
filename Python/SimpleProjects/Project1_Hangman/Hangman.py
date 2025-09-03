import random
from Hangman_Words import word_list
from Hangman_Art import stages, logo

reset_game = True

while reset_game:
    lives = 6

    print(logo)

    chosen_word = random.choice(word_list)

    placeholder = ""
    word_length = len(chosen_word)
    for position in range(word_length):
        placeholder += "_"
    print("Word to guess: " + placeholder)

    game_over = False
    correct_letters = []
    reset = ""

    while not game_over:
        print(f"****************************{lives}/6 LIVES LEFT****************************")
        guess = input("Guess a letter: ").lower()

        if guess in correct_letters:
            print(f"You've already guessed {guess}")

        display = ""

        for letter in chosen_word:
            if letter == guess:
                display += letter
                correct_letters.append(guess)
            elif letter in correct_letters:
                display += letter
            else:
                display += "_"

        print("Word to guess: " + display)

        if guess not in chosen_word:
            lives -= 1
            print(f"You guessed {guess}, that's not in the word. You lose a life.")
            if lives == 0:
                game_over = True
                print(stages[lives])
                print(f"***********************IT WAS {chosen_word}! YOU LOSE**********************")
                reset = input("Do you want play again? (y/n): ").lower()
                break

        if "_" not in display:
            game_over = True
            print(stages[lives])
            print("****************************YOU WIN****************************")
            reset = input("Do you want to play again? (y/n): ").lower()
            break

        print(stages[lives])

    if reset == "y":
        reset_game = True
    else:
        reset_game = False
