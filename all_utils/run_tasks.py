import os, sys, time
import datetime
import subprocess


def run_tasks(session_name, workdir, commands, servers, inavailable_gpus=None, required_mem_mb=40000, used_mem_torun_mb=10):

  # find idle gpus
  idle_gpus = []
  for server in servers:
    try:
      output = subprocess.check_output(
        f'ssh {server} nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv',
        shell=True).decode('utf-8')
      output = output.split('\n')[1:-1]
      # name, total mem, used mem
      for i, gpu in enumerate(output):
        name, total_mem, used_mem = gpu.split(',')
        total_mem = int(total_mem[:-3])
        used_mem = int(used_mem[:-3])
        if total_mem > int(required_mem_mb): # minimum requirement
          if used_mem < int(used_mem_torun_mb):
            for _server, _idx in inavailable_gpus:
              if (server==_server) and (i==int(_idx)): # not working gpu
                continue
            idle_gpus.append([server, i])
    except Exception as e:
      print(e)
      print(f"Error happens when searching idle GPUs on {server}.")

  # when there is no enough resource
  if len(idle_gpus) < len(commands):
    print("There are no GPUs to run the experiments")
    return False

  # create tmux session
  os.system(f"tmux new-session -s {session_name} -d")

  # create session
  for i, _command in enumerate(commands):
    server, gpu_idx = idle_gpus[i]
    os.system(f"tmux split-window -v -p 140 -t {session_name}")
    os.system(f'tmux send-keys -t {session_name}:0.{i+1} "ssh {server}" Enter')
    os.system(f'tmux send-keys -t {session_name}:0.{i+1} "cd {workdir}" Enter')
    os.system(f"""
      tmux send-keys -t {session_name}:0.{i+1} "CUDA_VISIBLE_DEVICES={gpu_idx} {_command}" Enter""")

  os.system(f'tmux send-keys -t {session_name}:0.0 "exit" Enter')
  os.system(f"tmux select-layout -t {session_name} even-vertical")


