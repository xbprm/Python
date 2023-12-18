import random

# colors is a list of available colors for the code
colors = ["R", "G" , "B", "Y", "P", "O"]

# code_length is the length of the code that the user must guess
code_length = 4

# max_attempts is the maximum number of attempts the user has to guess the code
max_attempts = 10

# generate a random code using the available colors and the code length
code = random.choices(colors, k=code_length)

# keep track of the number of attempts the user has made
attempts = 0

# print the code and some introductory text to the user
print(code)
print("The NeuralNine Mastermind Game")
print(f"Available colors: {', '.join(colors)}")
print(f"Code Length: {code_length}, Max Attempts: {max_attempts}")

# start the game loop, allowing the user to make attempts to guess the code
while attempts < max_attempts:
    # prompt the user to enter their guess
    guess = input(f"Attempt {attempts + 1} of {max_attempts}. Enter your guess:").strip().split()

    # check if the guess is valid (correct length and contains only available colors)
    if len(guess) != code_length or not all(color in colors for color in guess):
        print("Invalid guess! Make sure you have exactly 4 colors in your guess.")
        continue

    # count the number of correct positions and correct colors in the guess
    correct_position = sum(g == c for g, c in zip(guess, code))
    correct_color = sum(min(guess.count(c), code.count(c)) for c in set(code))
    correct_color -= correct_position

    # print the number of correct positions and correct colors to the user
    print(f"You have {correct_position} correct positions and {correct_color} correct colors.")

    # check if the user has won the game
    if correct_position == code_length:
        print("Congrats! You have won the game!")
        exit(0)

    # increment the number of attempts
    attempts += 1