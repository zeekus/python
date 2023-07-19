import os
import subprocess

def sayit(phrase):
    if os.path.exists("/usr/bin/festival"):
        cmd_talk = "festival --tts"
    elif os.path.exists("/usr/bin/espeak"):
        cmd_talk = "espeak -a 500 -p 1"
    else:
        print("Sorry, this program will not work without Festival or espeak installed. Please install one.\n")
        return

    cmd_echo = f'echo "{phrase}" | {cmd_talk}'

    text=f"debug: sayit: {cmd_echo}"
    log_event("raspberrypi", text) 

    try:
        status = subprocess.call(cmd_echo, stderr=subprocess.DEVNULL, shell=True)
    except Exception as e:
        traceback.print_exc()
        print(f"Error executing command: {e}")


hours=0
minutes=1
sayit_text=f"Be quiet. Go back to bed. There are {hours} hours and {minutes} minutes until morning."
sayit(sayit_text)
