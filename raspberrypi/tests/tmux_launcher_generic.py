import pexpect

def create_tmux_session(session_name, command):
    child = pexpect.spawn(f'tmux new-session -d -s {session_name} {command}')
    # Wait for the command to complete and the session to be ready
    child.expect_exact('Press Enter to continue...')
    # Detach from the session
    child.sendline('')
    # Close the child process
    child.close()

# Usage example
create_tmux_session('electronic_nanny', 'echo "hello world"; read -p "Press Enter to continue..."')

