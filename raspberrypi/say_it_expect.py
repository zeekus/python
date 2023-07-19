import expect

def sayit(phrase):
    if pexpect.which("festival"):
        cmd_talk = "festival --tts"
    elif pexpect.which("espeak"):
        cmd_talk = "espeak -a 500 -p 1"
    else:
        print("Sorry, this program will not work without Festival or espeak installed. Please install one.\n")
        return

    cmd_echo = f'echo "{phrase}" | {cmd_talk}'

    text = f"debug: sayit: {cmd_echo}"
    log_event("raspberrypi", text)

    try:
        child = pexpect.spawn('/bin/bash', ['-c', cmd_echo])
        child.expect(pexpect.EOF)
    except Exception as e:
        traceback.print_exc()
        print(f"Error executing command: {e}")