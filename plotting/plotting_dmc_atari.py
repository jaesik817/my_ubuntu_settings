import argparse
import collections
import functools
import json
import multiprocessing as mp
import pathlib
import re
import subprocess

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

import tensorboard as tb

# import matplotlib
# matplotlib.rcParams['mathtext.fontset'] = 'stix'
# matplotlib.rcParams['font.family'] = 'STIXGeneral'

Run = collections.namedtuple('Run', 'task method seed xs ys color')

"""
PALETTE = dict(
    transdreamer=(
        '#377eb8', '#4daf4a', '#984ea3', '#e41a1c', '#ff7f00', '#a65628',
        '#f781bf', '#888888', '#a6cee3', '#b2df8a', '#cab2d6', '#fb9a99',
    ),
    dreamer=(
        '#0022ff', '#33aa00', '#ff0011', '#ddaa00', '#cc44dd', '#0088aa',
        '#001177', '#117700', '#990022', '#885500', '#553366', '#006666',
    ),
    baselines=(
        '#222222', '#666666', '#aaaaaa', '#cccccc',
    ),
)
"""

PALETTE = 10 * (
    '#e41a1c', '#4daf4a', '#377eb8', '#984ea3', '#ff7f00', '#a65628',
    '#f781bf', '#888888', '#a6cee3', '#b2df8a', '#cab2d6', '#fb9a99',
    '#fdbf6f')

LEGEND = dict(
    fontsize='medium', numpoints=1, labelspacing=0, columnspacing=1.2,
    handlelength=1.5, handletextpad=0.5, ncol=5, loc='lower center')


def find_keys(args):
  filename = next(args.indir[0].glob('**/*.jsonl'))
  keys = set()
  for line in filename.read_text().split('\n'):
    if line:
      keys |= json.loads(line).keys()
  print(f'Keys ({len(keys)}):', ', '.join(keys), flush=True)


def load_runs(args):
  toload = []
  filenames = [pathlib.Path(__file__).parent / 'dmc_baselines' / 'dreamer.json']
  #for indir in args.indir:
  #  filenames = list(indir.glob('**/*.jsonl'))
  for filename in filenames:
    task, method, seed = filename.relative_to(indir).parts[:-1]
    if not any(p.search(task) for p in args.tasks):
      continue
    if not any(p.search(method) for p in args.methods):
      continue
    if method not in args.colors:
      args.colors[method] = args.palette[len(args.colors)]
    toload.append((filename, indir))
  print(f'Loading {len(toload)} of {len(filenames)} runs...')
  jobs = [functools.partial(load_run, f, i, args) for f, i in toload]
  with mp.Pool(10) as pool:
    promises = [pool.apply_async(j) for j in jobs]
    runs = [p.get() for p in promises]
  runs = [r for r in runs if r is not None]
  return runs


def load_run(filename, indir, args):
  task, method, seed = filename.relative_to(indir).parts[:-1]
  try:
    # Future pandas releases will support JSON files with NaN values.
    # df = pd.read_json(filename, lines=True)
    with filename.open() as f:
      df = pd.DataFrame([json.loads(l) for l in f.readlines()])
  except ValueError as e:
    print('Invalid', filename.relative_to(indir), e)
    return
  try:
    df = df[[args.xaxis, args.yaxis]].dropna()
  except KeyError:
    return
  xs = df[args.xaxis].to_numpy()
  ys = df[args.yaxis].to_numpy()
  color = args.colors[method]
  return Run(task, method, seed, xs, ys, color)


def atari_load_experiments(args):

  experiment = tb.data.experimental.ExperimentFromDev(args.atari_exp_id)
  df = experiment.get_scalars(include_wall_time=True)
  df = df[df.tag.str.contains('scalars/eval_return')]

  runs = []
  task_methods = df.run.apply(lambda run: '/'.join(run.split("/")[1:3])).unique()
  for _tm in task_methods:
    task = _tm.split('/')[0]
    if not re.compile(task) in args.atari_tasks:
      continue
    method = _tm.split('/')[-1]
    _df = df[df.run.str.contains(task)]
    _df = _df[_df.run.str.contains(method)]
    seeds = _df.run.apply(lambda run: run.split("/")[-1]).unique()
    for _seed in seeds:
      __df = _df[_df.run.str.contains('/'+_seed)]
      xs = pd.DataFrame(__df['step']).to_numpy()
      ys = pd.DataFrame(__df['value']).to_numpy()
      if 'dreamerv2' in method:
        _method = 'Dreamer(V2)fromCodes'
      else:
        _method = 'Dreamer-torch'
      if _method not in args.colors:
        args.colors[_method] = args.palette[len(args.colors)]
      color = args.colors[_method]
      runs.append(Run(task, _method, _seed, xs, ys, color))
  return runs

def dmc_load_experiments(args):

  experiment = tb.data.experimental.ExperimentFromDev(args.dmc_exp_id)
  df = experiment.get_scalars(include_wall_time=True)
  df = df[df.tag.str.contains('scalars/eval_return')]

  runs = []
  task_methods = df.run.apply(lambda run: '/'.join(run.split("/")[1:3])).unique()
  for _tm in task_methods:
    task = _tm.split('/')[0]
    if not re.compile(task) in args.dmc_tasks:
      continue
    method = _tm.split('/')[-1]
    _df = df[df.run.str.contains(task)]
    _df = _df[_df.run.str.contains(method)]
    seeds = _df.run.apply(lambda run: run.split("/")[-1]).unique()
    for _seed in seeds:
      __df = _df[_df.run.str.contains('/'+_seed)]
      xs = pd.DataFrame(__df['step']).to_numpy()
      ys = pd.DataFrame(__df['value']).to_numpy()
      if 'dreamerv2' in method:
        _method = 'Dreamer(V2)fromCodes'
      else:
        _method = 'Dreamer-torch'
      if _method not in args.colors:
        args.colors[_method] = args.palette[len(args.colors)]
      color = args.colors[_method]
      runs.append(Run(task, _method, _seed, xs, ys, color))
  return runs


def atari_load_dreamers(args):
  runs = []
  filename = pathlib.Path(__file__).parent / 'atari_baselines' / 'atari-dreamerv2.json'
  data = json.loads(filename.read_text())
  for _data in data:
    task = _data['task']
    method = _data['method']
    if not re.compile(task) in args.atari_tasks:
      continue
    if method != 'dreamerv2':
      continue
    else:
      method = 'Dreamer(V2)onPaper'
    seed = _data['seed']
    xs = pd.DataFrame(_data['xs']).to_numpy()
    ys = pd.DataFrame(_data['ys']).to_numpy()
    if method not in args.colors:
      #args.colors[method] = args.palette['dreamer'][len(args.colors)]
      args.colors[method] = args.palette[len(args.colors)]
    color = args.colors[method]
    runs.append(Run(task, method, seed, xs, ys, color))
  return runs


def dmc_load_dreamers(args):
  runs = []
  filename = pathlib.Path(__file__).parent / 'dmc_baselines' / 'dreamer.json'
  data = json.loads(filename.read_text())
  for _data in data:
    task = _data['task']
    method = _data['method']
    seed = _data['seed']
    if not re.compile(task) in args.dmc_tasks:
      continue
    if method == 'dreamer':
      method = 'Dreamer(V2)onPaper'
    xs = pd.DataFrame(_data['xs']).to_numpy()
    ys = pd.DataFrame(_data['ys']).to_numpy()
    if method not in args.colors:
      args.colors[method] = args.palette[len(args.colors)]
    color = args.colors[method]
    runs.append(Run(task, method, seed, xs, ys, color))
  return runs



def load_baselines_detail(args):
  runs = []
  filename = pathlib.Path(__file__).parent / 'atari_baselines' / 'atari-dopamine.json'
  data = json.loads(filename.read_text())
  for _data in data:
    task = _data['task']
    method = _data['method']
    if not re.compile(task) in args.tasks:
      continue
    if not re.compile(method) in args.baselines:
      continue
    if method == 'dqn_sticky':
      method = 'DQN'
    elif method == 'iqn_sticky':
      method = 'IQN'
    elif method == 'rainbow_sticky':
      method = 'Raindow'
    seed = _data['seed']
    xs = pd.DataFrame(_data['xs']).to_numpy()
    ys = pd.DataFrame(_data['ys']).to_numpy()
    if method not in args.colors:
      #args.colors[method] = args.palette['dreamer'][len(args.colors)]
      args.colors[method] = args.palette[len(args.colors)]
    color = args.colors[method]
    runs.append(Run(task, method, seed, xs, ys, color))
  return runs


def load_baselines(args):
  runs = []
  filename = pathlib.Path(__file__).parent / 'atari_baselines' / 'baselines.json'
  for task, methods in json.loads(filename.read_text()).items():
    if not re.compile(task) in args.tasks:
      continue
    for method, score in methods.items():
      if not any(p.search(method) for p in args.baselines):
        continue
      if method == 'iqn_sticky_2e8':
        method = 'IQN (2e8 steps)'
      elif method == 'raindow_sticky_2e8':
        method = 'Rainbow (2e8 steps)'
      if method not in args.colors:
        #args.colors[method] = args.palette['baselines'][len(args.colors)]
        args.colors[method] = args.palette[len(args.colors)]
      color = args.colors[method]
      runs.append(Run(task, method, None, None, score, color))
  return runs


def stats(runs):
  baselines = sorted(set(r.method for r in runs if r.xs is None))
  runs = [r for r in runs if r.xs is not None]
  tasks = sorted(set(r.task for r in runs))
  methods = sorted(set(r.method for r in runs))
  seeds = sorted(set(r.seed for r in runs))
  print('Loaded', len(runs), 'runs.')
  print(f'Tasks     ({len(tasks)}):', ', '.join(tasks))
  print(f'Methods   ({len(methods)}):', ', '.join(methods))
  print(f'Seeds     ({len(seeds)}):', ', '.join(seeds))
  print(f'Baselines ({len(baselines)}):', ', '.join(baselines))


def figure(runs, args):
  tasks = sorted(set(r.task for r in runs if r.xs is not None))
  rows = int(np.ceil(len(tasks) / args.cols))
  figsize = args.size[0] * args.cols, args.size[1] * rows
  fig, axes = plt.subplots(rows, args.cols, figsize=figsize)
  for task, ax in zip(tasks, axes.flatten()):
    relevant = [r for r in runs if r.task == task]
    plot(task, ax, relevant, args)
  for ax in axes.flatten():
    ax.xaxis.get_offset_text().set_visible(False)
  axes[0,-1].xaxis.get_offset_text().set_visible(True)
  axes[1,-1].xaxis.get_offset_text().set_visible(True)
  #if args.xlim:
  #  for ax in axes[:-1].flatten():
  #    ax.xaxis.get_offset_text().set_visible(False)
  if args.xlabel:
    if len(axes.shape) == 1:
      for ax in axes:
        ax.set_xlabel(args.xlabel, fontsize=8)
    else:
      for ax in axes[-1]:
        ax.set_xlabel(args.xlabel, fontsize=8)
  if args.ylabel:
    if len(axes.shape) == 1:
      axes[0].set_ylabel(args.ylabel)
    else:
      for ax in axes[:, 0]:
        ax.set_ylabel(args.ylabel)
  for ax in axes[len(tasks):]:
    ax.axis('off')
  legend(fig, args.labels, **LEGEND)
  return fig


def plot(task, ax, runs, args):
  try:
    title = task.split('_', 1)[1].replace('_', ' ').title()
  except IndexError:
    title = task.title()
  ax.set_title(title)
  methods = []
  methods += sorted(set(r.method for r in runs if r.xs is not None))
  methods += sorted(set(r.method for r in runs if r.xs is None))
  xlim = [+np.inf, -np.inf]
  for index, method in enumerate(methods):
    relevant = [r for r in runs if r.method == method]
    if not relevant:
      continue
    if any(r.xs is None for r in relevant):
      baseline(index, method, ax, relevant, args)
    else:
      if args.aggregate == 'std':
        xs, ys = curve_std(task, index, method, ax, relevant, args)
      elif args.aggregate == 'none':
        xs, ys = curve_individual(task, index, method, ax, relevant, args)
      else:
        raise NotImplementedError(args.aggregate)
      xlim = [min(xlim[0], xs.min()), max(xlim[1], xs.max())]
  ax.ticklabel_format(axis='x', style='sci', scilimits=(0, 0))
  steps = [1, 2, 2.5, 5, 10]
  ax.xaxis.set_major_locator(ticker.MaxNLocator(args.xticks, steps=steps))
  ax.yaxis.set_major_locator(ticker.MaxNLocator(args.yticks, steps=steps))
  if 'dmc' in task:
    task_xlim = args.dmc_xlim
  else:
    task_xlim = args.atari_xlim
  ax.set_xlim(task_xlim or xlim)
  if task_xlim:
    ticks = sorted({*ax.get_xticks(), * task_xlim})
    ticks = [x for x in ticks if task_xlim[0] <= x <= task_xlim[1]]
    ax.set_xticks(ticks)
  if args.ylim:
    ax.set_ylim(args.ylim)
    ticks = sorted({*ax.get_yticks(), *args.ylim})
    ticks = [x for x in ticks if args.ylim[0] <= x <= args.ylim[1]]
    ax.set_yticks(ticks)


def curve_individual(index, method, ax, runs, args):
  if 'dmc' in task:
    task_bins = args.dmc_bins
  else:
    task_bins = args.atari_bins
  if task_bins:
    for index, run in enumerate(runs):
      xs, ys = binning(run.xs, run.ys, task_bins, np.nanmean)
      runs[index] = run._replace(xs=xs, ys=ys)
  zorder = 10000 - 10 * index - 1
  for run in runs:
    ax.plot(run.xs, run.ys, label=method, color=run.color, zorder=zorder)
  return runs[0].xs, runs[0].ys


def curve_std(task, index, method, ax, runs, args):
  if 'dmc' in task:
    task_bins = args.dmc_bins
  else:
    task_bins = args.atari_bins
  if task_bins:
    for index, run in enumerate(runs):
      xs, ys = binning(run.xs, run.ys, task_bins, np.nanmean)
      runs[index] = run._replace(xs=xs, ys=ys)
  xs = np.concatenate([r.xs for r in runs])
  ys = np.concatenate([r.ys for r in runs])
  order = np.argsort(xs)
  xs, ys = xs[order], ys[order]
  color = runs[0].color
  if task_bins:
    reducer = lambda y: (np.nanmean(np.array(y)), np.nanstd(np.array(y)))
    xs, ys = binning(xs, ys, task_bins, reducer)
    ys, std = ys.T
    kw = dict(color=color, zorder=10000 - 10 * index, alpha=0.1, linewidths=0)
    ax.fill_between(xs, ys - std, ys + std, **kw)
  ax.plot(xs, ys, label=method, color=color, zorder=10000 - 10 * index - 1)
  return xs, ys


def baseline(index, method, ax, runs, args):
  assert len(runs) == 1 and runs[0].xs is None
  y = np.mean(runs[0].ys)
  kw = dict(ls='--', color=runs[0].color, zorder=5000 - 10 * index - 1)
  ax.axhline(y, label=method, **kw)


def binning(xs, ys, bins, reducer):
  binned_xs = np.arange(xs.min(), xs.max() + 1e-10, bins)
  binned_ys = []
  for start, stop in zip([-np.inf] + list(binned_xs), binned_xs):
    left = (xs <= start).sum()
    right = (xs <= stop).sum()
    binned_ys.append(reducer(ys[left:right]))
  binned_ys = np.array(binned_ys)
  return binned_xs, binned_ys


def legend(fig, mapping=None, **kwargs):
  entries = {}
  for ax in fig.axes:
    for handle, label in zip(*ax.get_legend_handles_labels()):
      if mapping and label in mapping:
        label = mapping[label]
      entries[label] = handle
  leg = fig.legend(entries.values(), entries.keys(), **kwargs)
  leg.get_frame().set_edgecolor('white')
  extent = leg.get_window_extent(fig.canvas.get_renderer())
  extent = extent.transformed(fig.transFigure.inverted())
  yloc, xloc = kwargs['loc'].split()
  y0 = dict(lower=extent.y1, center=0, upper=0)[yloc]
  y1 = dict(lower=1, center=1, upper=extent.y0)[yloc]
  x0 = dict(left=extent.x1, center=0, right=0)[xloc]
  x1 = dict(left=1, center=1, right=extent.x0)[xloc]
  fig.tight_layout(rect=[x0, y0, x1, y1], h_pad=0.5, w_pad=2.0)


def save(fig, args):
  args.outdir.mkdir(parents=True, exist_ok=True)
  filename = args.outdir / f'{args.fig_name}.png'
  fig.savefig(filename, dpi=130)
  print('Saved to', filename)
  filename = args.outdir / f'{args.fig_name}.pdf'
  fig.savefig(filename)
  try:
    subprocess.call(['pdfcrop', str(filename), str(filename)])
  except FileNotFoundError:
    pass  # Install texlive-extra-utils.


def main(args):
  #find_keys(args)
  #runs = load_runs(args) + load_baselines(args)
  runs = atari_load_experiments(args)
  runs += atari_load_dreamers(args)
  runs += dmc_load_experiments(args)
  runs += dmc_load_dreamers(args)
  #runs += load_baselines_detail(args)
  stats(runs)
  if not runs:
    print('Noting to plot.')
    return
  print('Plotting...')
  fig = figure(runs, args)
  save(fig, args)


def parse_args():
  boolean = lambda x: bool(['False', 'True'].index(x))
  parser = argparse.ArgumentParser()
  parser.add_argument('--indir', nargs='+', type=pathlib.Path, required=True)
  parser.add_argument('--outdir', type=pathlib.Path, required=True)
  parser.add_argument('--subdir', type=boolean, default=False)
  parser.add_argument('--xaxis', type=str, required=True)
  parser.add_argument('--yaxis', type=str, required=True)
  parser.add_argument('--dmc_tasks', nargs='+', default=[r'.*'])
  parser.add_argument('--atari_tasks', nargs='+', default=[r'.*'])
  parser.add_argument('--methods', nargs='+', default=[r'.*'])
  parser.add_argument('--baselines', nargs='+', default=[])
  parser.add_argument('--dmc_bins', type=float, default=0)
  parser.add_argument('--atari_bins', type=float, default=0)
  parser.add_argument('--aggregate', type=str, default='std')
  parser.add_argument('--size', nargs=2, type=float, default=[2.5, 2.3])
  parser.add_argument('--cols', type=int, default=4)
  parser.add_argument('--dmc_xlim', nargs=2, type=float, default=None)
  parser.add_argument('--atari_xlim', nargs=2, type=float, default=None)
  parser.add_argument('--ylim', nargs=2, type=float, default=None)
  parser.add_argument('--xlabel', type=str, default=None)
  parser.add_argument('--ylabel', type=str, default=None)
  parser.add_argument('--xticks', type=int, default=6)
  parser.add_argument('--yticks', type=int, default=5)
  parser.add_argument('--labels', nargs='+', default=None)
  parser.add_argument('--palette', nargs='+', default=PALETTE)
  parser.add_argument('--colors', nargs='+', default={})
  parser.add_argument('--dmc_exp_id', type=str, default=None)
  parser.add_argument('--atari_exp_id', type=str, default=None)
  parser.add_argument('--fig_name', type=str, default=None)
  args = parser.parse_args()
  if args.subdir:
    args.outdir /= args.indir[0].stem
  args.indir = [d.expanduser() for d in args.indir]
  args.outdir = args.outdir.expanduser()
  if args.labels:
    assert len(args.labels) % 2 == 0
    args.labels = {k: v for k, v in zip(args.labels[:-1], args.labels[1:])}
  if args.colors:
    assert len(args.colors) % 2 == 0
    args.colors = {k: v for k, v in zip(args.colors[:-1], args.colors[1:])}
  args.atari_tasks = [re.compile(p) for p in args.atari_tasks]
  args.dmc_tasks = [re.compile(p) for p in args.dmc_tasks]
  args.methods = [re.compile(p) for p in args.methods]
  args.baselines = [re.compile(p) for p in args.baselines]
  args.palette = 10 * args.palette
  return args


if __name__ == '__main__':
  main(parse_args())
