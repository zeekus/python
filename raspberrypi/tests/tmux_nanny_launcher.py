#!/usr/bin/python3
#filename: tmux_nanny_launcher.py
#description: a wrapper file to launch the night_time_nanny.py script from bash like a human
#requirements tmux and pexpect
import pexpect

#start a new tmux session
child = pexpect.spawn("tmux new-session -s nighttime_nanny")

# Wait for the tmux prompt to appear (ending with $)
prompt_pattern = r'.*\$'
child.expect(prompt_pattern)

#run night time nanny program
child.sendline('nohup python3 night_time_nanny.py &')

#detach from the session
child.expect('tmux detach')

#end process
child.expect(pexpect.EOF)

#show output
print(child.before)
