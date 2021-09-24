#!/bin/zsh

if [ $1 = "dev" ]
then
  session_name='tbdev-'$2
else
  session_name='tb-'$1'-'$2
fi

tmux new-session -s $session_name -d
tmux split-window -v -p 140 -t $session_name

if [ $1 = "dev" ]
then
  tmux send-keys -t $session_name:0.1 "tensorboard dev upload --logdir=/common/home/jy651/$2 --name $2" Enter
  #tmux send-keys -t $session_name:0.1 "tensorboard dev upload --logdir=/common/users/jy651/$2 --name $2" Enter
else
  tmux send-keys -t $session_name:0.1 "tensorboard --logdir=/common/users/jy651/$1 --host 0.0.0.0 --port $2" Enter
fi

tmux select-layout -t $session_name tiled
