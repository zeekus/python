#!/usr/bin/env python3
"""
A simple shell script meditation helper.
Author: Teddy Knab
Date: 04-03-2003
"""

import sys
import subprocess
import time
import os.path
import argparse


def print_message(message):
    """
    Prints a message to the console and speaks it using text-to-speech.
    """
    print(message)

    if os.path.exists("/usr/bin/festival"):
        # if festival is available, use it
        cmd_talk = "festival --tts"
        subprocess.call(f"echo '{message}' | {cmd_talk}", shell=True)
    elif os.path.exists("/usr/bin/espeak"):
        # if espeak is available, use it
        cmd_talk = "espeak -a 500 -p 1"
        subprocess.call(f"echo '{message}' | {cmd_talk}", shell=True)
    else:
        print("Sorry, this program requires festival or espeak to be installed.")


def wait(minutes):
    """
    Pauses the program for the specified number of minutes.
    """
    print(f"Waiting for {minutes} minutes...")
    seconds = minutes * 60
    time.sleep(seconds)


def main():
    """
    The main function that runs the meditation guide.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--timeblock",
        "-b",
        type=int,
        default=10,
        help="The amount of time available for meditation in minutes.",
    )
    args = parser.parse_args()

    time_available = args.timeblock
    main_wait = max(time_available - 6, 0)

    print(f"Welcome to your {time_available}-minute meditation.")
    print(f"The main meditation time will be {main_wait} minutes.")

    # modify these if you want to change the wait times (in minutes)
    wait_times_for_each_sequence = [
        0.25,  # 1
        0.25,  # 2
        2,  # 3
        0.5,  # 4
        1,  # 5
        main_wait,  # 6 main meditation sequence
        1,  # 7
        0,  # 8 meditation sequences
    ]

    # modify these if you want to change the messages
    mediation_playbook = [
        "Get settled and close your eyes.",
        "Bring your attention to your body.",
        "Scan through your body from head to toe.",
        "Set your intentions for this meditation session.",
        "Focus your attention on the space around you.",
        "Focus your attention on your breathing. Count your breaths. Let your mind wander if it wants to.",
        "Focus your attention on the space around you.",
        "Thank yourself and the universe. Open your eyes.",
    ]

    for count, (sequ, message) in enumerate(zip(wait_times_for_each_sequence, mediation_playbook)):
        print(f"Step {count + 1}: {message}")
        print_message(message)
        wait(sequ)

    print("Your meditation session is now complete.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)
