import os, sys
import inspect

def main(*argv):
  if not argv:
    argv = list(sys.argv)[1:]
  if argv[0] == 'stat':
    path = os.path.dirname(inspect.getfile(inspect.currentframe()))
    os.system("zsh "+os.path.join(path,"server_stats.sh ")+ ' '.join(argv[1:]))
