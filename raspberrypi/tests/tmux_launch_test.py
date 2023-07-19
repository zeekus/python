#!/usr/bin/python3


import pexpect
import subprocess

def check_tmux_installed():
    try:
        subprocess.check_call(['tmux', '-V'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def start_tmux_server():
    try:
        subprocess.check_output(['tmux', 'start-server'], stderr=subprocess.STDOUT)
        print("tmux server started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while starting tmux server: {e}")

def check_tmux_server_running():
    try:
        subprocess.check_output(['tmux', 'ls'], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False


def create_tmux_session(session_name, command):
    if not check_tmux_installed():
        print("Error: tmux is not installed. Please install tmux to continue.")
        return

    if not check_tmux_server_running():
        start_tmux_server()

    try:
        child = pexpect.spawn(f'tmux new-session -d -s {session_name} {command}')
        # Wait for the command to complete and the session to be ready
        child.expect_exact('Press Enter to continue...')
        # Detach from the session
        child.sendline('')
        # Wait for the session to be detached
        child.expect(pexpect.EOF)
        # Check the exit status of the spawned process
        if child.exitstatus == 0:
            print(f"Session '{session_name}' created successfully.")
        else:
            print(f"Error occurred while creating session '{session_name}'.")
        # Close the child process
        child.close()
    except pexpect.ExceptionPexpect as e:
        print(f"An error occurred: {e}")


# Usage example
create_tmux_session('electronic_nanny', 'echo "hello world"; read -p "Press Enter to continue..."')