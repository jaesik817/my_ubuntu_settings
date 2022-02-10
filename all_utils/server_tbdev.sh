#!/bin/zsh

#session_name=tbdev
#exp_id=lpJyVY4BQuOr2cbktxuDtA
#model_dir=transdreamer-torch

session_name=tbdev_minigrid
exp_id=MSrbE161RjqNz0ZhmqXnMQ
model_dir=transdreamer-minigrid

servers=(welling bengio hinton sutton jordan jurgen rumelhart)

tmux new-session -s $session_name -d
for i in {1..${#servers[@]}}
do
  server=${servers[$i]}
  tmux split-window -v -p 140 -t $session_name
  tmux send-keys -t $session_name:0.$i "ssh $server" Enter
  if [ $server = "jordan" ]
  then
    logdir_root='/data/sdb/local/jy651/'
  else
    logdir_root='/data/local/jy651/'
  fi  
  tmux send-keys -t $session_name:0.$i "cd $logdir_root" Enter
  tmux send-keys -t $session_name:0.$i "hostname" Enter
  tmux send-keys -t $session_name:0.$i "ll" Enter
  tmux send-keys -t $session_name:0.$i "tensorboard dev upload --logdir $model_dir/logdir/ --experiment_id $exp_id" Enter
done
tmux select-layout -t $session_name tiled
