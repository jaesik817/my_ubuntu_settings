import os
import subprocess

returned_value = subprocess.check_output('tensorboard dev list', shell=True).decode('utf-8').split('\n')[:-1]

num_lines_per_log = 11
num_exps = int(len(returned_value)/num_lines_per_log)
exps = []
for i in range(num_exps):
  _exp = {}
  _exp['name'] = returned_value[i*num_lines_per_log + 1].split(' ')[-1]
  _exp['description'] = returned_value[i*num_lines_per_log + 2].split(' ')[-1]
  _exp['id'] = returned_value[i*num_lines_per_log + 3].split(' ')[-1]
  _exp['runs'] = float(returned_value[i*num_lines_per_log + 6].split(' ')[-1])
  _exp['scalars'] = float(returned_value[i*num_lines_per_log + 8].split(' ')[-1])
  exps.append(_exp)

# remove empty experiments and print valid experiments
total_scalars = 0
for _exp in exps:
  if _exp['runs'] == 0:
    _id = _exp['id']
    os.system(f"tensorboard dev delete --experiment_id {_id}")
  else:
    print(f"Experiment {_exp['name']}")
    print(f"    ID: {_exp['id']}")
    print(f"    runs: {_exp['runs']}")
    print(f"    scalars: {_exp['scalars']}")
    total_scalars += _exp['scalars']

# total scalars
total_scalars = total_scalars/1000/1000
print(f"Total scalars(Maximum 100M): {total_scalars}M")

