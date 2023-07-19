#sayit sends computer voice through the speakers
def sayit(phrase):
    cmd_echo = f'echo "{phrase}"'

    text=f"debug: sayit: {cmd_echo}"
    log_event("raspberrypi", text) 

    if os.path.exists("/usr/bin/festival"):
        cmd_talk = "festival --tts"
        #errors get chatty so I am sending them to devnull
        try:
            status = subprocess.call(cmd_echo + "|" + cmd_talk, stderr=subprocess.DEVNULL, shell=True)
        except Exception as e:
            traceback.print_exc()
            print(f"Error executing festival command: {e}")
    elif os.path.exists("/usr/bin/espeak"):
        cmd_talk = "espeak -a 500 -p 1 "
        try:
            status = subprocess.call(cmd_echo + "|" + cmd_talk, stderr=subprocess.DEVNULL, shell=True)
        except Exception as e:
            traceback.print_exc()
            print(f"Error executing espeak command: {e}")
    else:
        print("Sorry, this program will not work without Festival or espeak installed. Please install one.\n")
        sys.exit(1)


hours=0
minutes=1
sayit_text=f"Be quiet. Go back to bed. There are {hours} hours and {minutes} minutes until morning."
sayit(sayit_text)
