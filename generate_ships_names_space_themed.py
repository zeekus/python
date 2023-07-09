#!/usr/bin/python3
#filename: generate_ships_names_space_themed.py
#description: The program finds all 3-number combinations that sum to 15 and associates each with a random space-themed word.
"""
The Python program is designed to find all possible combinations of three numbers that add up to 15, with the range of numbers from 0 to 9, including repeated numbers like 555. The program uses a recursive function to generate all possible combinations of numbers and a list of space-themed words to associate with each combination. The program randomly selects a different space-themed word for each combination of numbers and prints the combination and the associated word. The program also includes comments to explain each part of the code and make it easier to understand and modify.
"""

import random


# Function to return a list of space-themed words
def space_themed_words():
    return [
        "sky",
        "moon",
        "star",
        "comet",
        "orbit",
        "lunar",
        "solar",
        "mars",
        "venus",
        "jupit",
        "pluto",
        "nebul",
        "cosmic",
        "meteor",
        "orbits",
        "comets",
        "saturn",
        "uranus",
        "neptune",
        "jupiter",
        "nebula",
        "planets",
        "galaxy",
        "cosmos",
        "bigbang",
        "gravity",
        "stellar",
        "quasars",
        "pulsars",
        "astronomy",
        "telescope",
        "blackhole",
    ]

# Function to return a random index from the space-themed words list
def random_space_word():
    words = space_themed_words()
    return random.choice(range(len(words)))

# Recursive function to find all combinations of numbers that add up to the target sum
def random_space_word_index():
    words=space_themed_words()
    return random.choice(range(len(words)))


def find_combinations(target_sum, num_count, start=0, combination=[]):
    # Base case: when the number count reaches 0
    if num_count == 0:
        # Check if the current combination adds up to the target sum
        if target_sum == 0:
            # Get a random index for a space-themed word
            word_index  = random_space_word_index()
            # Select the word using the random index
            word = space_themed_words()[word_index]
            # Convert the combination of numbers to a string
            str_combination="".join(str(num) for num in combination)
            # Print the combination and the associated space-themed word
            print(str_combination, word)
        return

    # Iterate through the numbers in the specified range
    for i in range(start, 10):
        # If the target sum minus the current number is negative, break the loop
        if target_sum - i < 0:
          break
        #find_combinations(target_sum - i, num_count - 1, i + 1, combination + [i])

        #find all combinations with out every order
        #find_combinations(target_sum - i, num_count - 1, i, combination + [i])

        #all combinations in every order
        # Recursively call the function with the updated target sum, number count, and combination
        find_combinations(target_sum - i, num_count - 1, 0, combination + [i])

#Main part of the program
if __name__ == "__main__":
    #Set the target sum and number count
    target_sum = 15
    num_count = 3
    # Call the find combinations function and print all the combinations and their associated space-themed words
    find_combinations(target_sum, num_count)
