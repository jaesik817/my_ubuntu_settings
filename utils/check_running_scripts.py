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

# find running python scripts
for server in servers:
  print(server)
  try:
    output = subprocess.check_output(
      f'ssh {server} ps -ef |grep jy651 | grep python'+grep_strs,
      shell=True).decode('utf-8')
    print(output)
  except:
    print('')
  
