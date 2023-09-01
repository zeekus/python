#!/usr/bin/python3
#filename: lucky_lamda_mm.py
#description: generate a lucky mega million pick

import random

white_balls = lambda: random.sample(range(1, 70), 5)
gold_ball = lambda: random.sample(range(1, 25), 1)
sorted_white_balls=sorted(white_balls())
print(f"Your lucky mega millions number is {sorted_white_balls} gold ball: {gold_ball()}" )