#!/bin/zsh

session_name=stats
servers=(hinton bengio lecun)

echo $servers
tmux new-session -s $session_name -d
for i in {1..${#servers[@]}}
do
  server=${servers[$i]}
  tmux split-window -v -p 140 -t $session_name
  tmux send-keys -t $session_name:0.$i "ssh $server" Enter
  #tmux send-keys -t $session_name:0.$i "gpustat --watch" Enter
  tmux send-keys -t $session_name:0.$i '
    total_cpu_num=$(grep -c processor /proc/cpuinfo)
    total_mem=$(awk '"'"'/MemTotal/ {print $2/1024/1024}'"'"' /proc/meminfo)
    while
    do
      gpustat
      echo "CPU("$total_cpu_num") Usage: " $(grep cpu /proc/stat | awk '"'"'{usage=($2+$4)*100/($2+$4+$5)} END {print usage "%"}'"'"')
      used_mem=$(awk '"'"'/MemAvailable/ {print $2/1024/1024}'"'"' /proc/meminfo)
      echo "Memory("$total_mem"GB) Usage: "$(($total_mem - $used_mem))"GB"
      df -h |grep data
      sleep 5
      clear
    done
  ' Enter
done
if [ $1 = "all" ]
then
  tmux send-keys -t $session_name:0.0 "ssh welling" Enter
  tmux send-keys -t $session_name:0.0 "cd /common/users/" Enter
  tmux send-keys -t $session_name:0.0 "while; do; quota -vs; sleep 2; clear; done" Enter
else
  tmux send-keys -t $session_name:0.0 "exit" Enter
fi
tmux select-layout -t $session_name tiled
