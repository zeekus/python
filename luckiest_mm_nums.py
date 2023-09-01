#!/usr/bin/python3
#filename: luckiest_mm_nums.py
#description: create a bunch of mega million random pick based on the mega million ruleset

import random

checks = 10000000
white_balls = lambda: random.sample(range(1, 70), 5)
gold_ball = lambda: random.sample(range(1, 25), 1)

mega_num_picks = []
gold_num_picks = []
print (f"Running {checks} loops to get random numbers")
for i in range(checks):
    mega_num_picks.append(white_balls())
    gold_num_picks.append(gold_ball())


lucky_main_numbers={}
for numbers in mega_num_picks:
    numbers = tuple(sorted(numbers))
    if numbers in lucky_main_numbers:
        lucky_main_numbers[numbers] += 1
    else:
        lucky_main_numbers[numbers] = 1

lucky_gold_numbers={}
for numbers in gold_num_picks:
    numbers = tuple(sorted(numbers))
    if numbers in lucky_gold_numbers:
        lucky_gold_numbers[numbers] += 1
    else:
        lucky_gold_numbers[numbers] = 1



most_lucky_main_numbers = sorted(lucky_main_numbers.items(), key=lambda x: x[1], reverse=True)[:1]
most_lucky_gold_numbers = sorted(lucky_gold_numbers.items(), key=lambda x: x[1], reverse=True)[:1]

print("The luckiest lucky numbers are:")
for numbers, count in most_lucky_main_numbers:
    print(numbers, "appeared", count, "times")

for gold_numbers, count in most_lucky_gold_numbers:
    gold_num_str=str(gold_numbers).replace(",","")
    print(f"{gold_num_str} gold ball appeared  {count} times")

