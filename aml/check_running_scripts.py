import os, sys, time
import datetime
import gpustat
import subprocess

try:
  keywords = sys.argv[1].split(',')
  grep_strs = ''
  for _keyword in keywords:
    grep_strs +=f'|grep {_keyword} '
except:
  grep_strs = ''

servers = [
    #'welling', # gpus are inavailable
    'hinton', # 24GB
    'sutton',
    'jurgen', # 16GB
    'bengio', # 48GB
    'jordan',
    'rumelhart',
]

## find idle gpus
#min_required_mem = 10000
#used_mem_threshold = 300
#gpu_summary = {}
#idle_gpus = []
#for server in servers:
#  try:
#    output = subprocess.check_output(
#      f'ssh {server} nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv',
#      shell=True).decode('utf-8')
#    # name, total mem, used mem
#    output = output.split('\n')[1:-1]
#    for i, gpu in enumerate(output):
#      name, total_mem, used_mem = gpu.split(',')
#      total_mem = int(total_mem[:-3])
#      used_mem = int(used_mem[:-3])
#      if not name+' '+str(total_mem)+'MB' in gpu_summary.keys():
#        gpu_summary[name+' '+str(total_mem)+'MB'] = 0
#      if total_mem > min_required_mem: # minimum requirement
#        if used_mem < used_mem_threshold:
#          if (server=='hinton') and (i==4): # not working gpu
#            continue
#          if (server=='bengio') and (i==5): # not working gpu
#            continue
#          idle_gpus.append([server, total_mem, i])
#          gpu_summary[name+' '+str(total_mem)+'MB'] += 1
#  except:
#    print(f'{server} gpus are inavailable')


# find running python scripts
processes = {}
for server in servers:
  try:
    output = subprocess.check_output(
      f'ssh {server} ps -ef |grep jy651 | grep python'+grep_strs,
      shell=True).decode('utf-8')
    output = output.split('\n')[:-1]
    processes[server] = output
  except:
    print('')

#print("Idle GPUs")
#for key, value in gpu_summary.items():
#  if value != 0:
#    print(key, value)
print("Processes")
for server, procs in processes.items():
  print(server)
  for _proc in procs:
    print('    ',_proc)

