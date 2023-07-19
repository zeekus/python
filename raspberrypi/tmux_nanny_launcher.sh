#!/bin/bash
#filename: tmux_nanny_launcher.sh
#description: a wrapper file to launch the night_time_nanny.py script from bash like a human
#requirements tmux and pexpect (installed with Python3)

# Start a new tmux session
tmux new-session -d -s nighttime_nanny

# Wait for the tmux prompt to appear (ending with $)
prompt_pattern=".*\$"
tmux send-keys -t nighttime_nanny "$prompt_pattern" Enter

# Run night time nanny program in the background
python3 /home/ted/night_time_nanny.py &

# Detach from the session
tmux send-keys -t nighttime_nanny "tmux detach" Enter

# Wait for the session to be detached
sleep 2

# End the tmux session
#tmux kill-session -t nighttime_nanny

# Show output (optional)
# To display the output, you can uncomment the following line
#tmux capture-pane -p -t nighttime_nanny

