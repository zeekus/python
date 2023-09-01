#!/usr/bin/python3
#filename: lucky_lamda_pb.py
#description: generate a lucky power ball ticket pick

import random

white_balls = lambda: random.sample(range(1, 69), 5)
red_ball = lambda: random.sample(range(1, 26), 1)
sorted_white_balls=sorted(white_balls())
print(f"Your lucky power ball number is {sorted_white_balls} red ball: {red_ball()}" )
