import random

colors = ["R", "G" , "B", "Y", "P", "O"]
code_length = 4
max_attempts = 10

code = random.choices(colors, k=code_length)
attempts = 0

print(code)

print("The NeuralNine Mastermind Game")
print(f"Avai1ab1e colors: {', '.join(colors)}")

print(f"Code Length: {code_length}, Max Attempts: {max_attempts}")

while attempts < max_attempts:
    guess = input(f"Attempt {attempts + 1} of {max_attempts}. Enter your guess:").strip().split()
    
    if len(guess)!= code_length or not all(color in colors for color in guess):
        print("Invalid guess! Make sure you have exactly 4 colors in your guess.")
        continue

    correct_position = sum(g == c for g, c in zip(guess, code))
    correct_color = sum(min(guess.count(c), code.count(c)) for c in set(code))
    correct_color -= correct_position                        

    print(f"You have {correct_position} correct positions and {correct_color} correct colors.")

    if correct_position == code_length:
        print("Congrats! You have won the game!")
        exit(0)

    attempts += 1