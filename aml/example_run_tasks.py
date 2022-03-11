import os, sys, time
import datetime
import subprocess
import aml


if __name__ == "__main__":

  # session_name
  date = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")
  session_name = 'dreamer-torch-dmc' + '-'+date

  # working folder
  working_dir = '~/dreamer-torch/'

  # commands
  commands = [
    'echo python dreamer.py --logdir logdir/dmc_walker_walk/dreamer-torch --config dmc --task dmc_walker_walk',
    'echo python dreamer.py --logdir logdir/dmc_cup_catch/dreamer-torch --config dmc --task dmc_cup_catch',
  ]

  # servers
  servers = [
    'hinton',
    'bengio',
    'lecun',
  ]

  # inavailable gpus
  inav_gpus = [
  ]

  # run
  aml.run_tasks(session_name, working_dir, commands, servers, inav_gpus, required_mem_mb=10000)
