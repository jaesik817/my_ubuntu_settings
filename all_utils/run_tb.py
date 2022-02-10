import os, sys
import datetime

target = sys.argv[1]

session_name = f'tbdev-{target}'

os.system(f'tmux new-session -s {session_name} -d')
os.system(f'tmux split-window -v -p 140 -t {session_name}')

if 'dreamer' in target:
  logdir = f'/common/users/jy651/{target}'
elif target == 'rl-starter-files':
  logdir = f'/common/home/jy651/{target}'
date = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")
os.system(f'tmux send-keys -t {session_name}:0.1 "tensorboard dev upload --logdir={logdir} --name {target}-{date}" Enter')

os.system(f'tmux select-layout -t {session_name} tiled')
