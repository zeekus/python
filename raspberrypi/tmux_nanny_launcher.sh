# Check if the session already exists
if ! tmux has-session -t nighttime_nanny 2>/dev/null; then
 # Start a new tmux session
 tmux new-session -s nighttime_nanny -n my_window -d bash
 # Wait for the tmux prompt to appear (ending with $)
 prompt_pattern=".*\$"
 tmux wait-for -S prompt_ready -t nighttime_nanny:my_window "$prompt_pattern"
fi
# Run nighttime nanny program in the background
#tmux send-keys -t nighttime_nanny:my_window "python3 /home/ted/night_time_nanny.py" Enter
tmux send-keys -t nighttime_nanny:my_window "python3 /home/ted/door_monitor_as_class.py" Enter
# Detach from the session
tmux send-keys -t nighttime_nanny:my_window "tmux detach" Enter
# Wait for the session to be detached
sleep 2 
