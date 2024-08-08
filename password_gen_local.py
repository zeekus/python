#!/usr/bin/python3
# filename: password_gen_local.py
# description: local random password generator

import random

# Character range function
def range_char(start, stop):
    return (chr(n) for n in range(ord(start), ord(stop) + 1))

def string_to_list(string):
    return [char for char in string]

def generate_password(length=48):
    mylist = []
    special_list = string_to_list('.!@#$^&*()')  # simplified special characters

    for character in range_char("a", "z"):
        mylist.append(character)
        mylist.append(character.upper())

    num = random.randrange(0, 10)  # corrected range to include 9
    char = random.choice(special_list)
    random.shuffle(mylist)

    pass_string = ''.join(mylist[:length])

    return f"{num}{pass_string}{char}"

if __name__ == "__main__":
    password = generate_password()
    print("Password is:", password)