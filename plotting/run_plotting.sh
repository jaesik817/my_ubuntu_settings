# Dreamer test
exp_id=i8mIqlUYSYOedQdLZ5AILg
python3 plotting_dmc_atari.py --indir ./logdir --outdir ./plots --xaxis step --yaxis test/return \
  --xlabel 'Environment Steps' --ylabel 'Episode Return' \
  --dmc_exp_id=$exp_id \
  --atari_exp_id=$exp_id \
  --dmc_xlim 0 5e6 --dmc_bins 1e5 \
  --atari_xlim 0 2e7 --atari_bins 1e6 \
  --size 3.0 2.5 --cols 5 \
  --dmc_tasks dmc_walker_walk dmc_pendulum_swingup dmc_cheetah_run dmc_cup_catch dmc_hopper_stand \
  --atari_tasks atari_boxing atari_freeway atari_pong  atari_krull atari_bank_heist \
  --fig_name dreamer-test

## TransDreamer-Atari-Chang
#exp_id=BojL5PgpQniqt13lIl5PvA
#python3 plotting_dmc_atari_chang.py --indir ./logdir --outdir ./plots --xaxis step --yaxis test/return \
#  --xlabel 'Environment Steps' --ylabel 'Episode Return' \
#  --dmc_exp_id=$exp_id \
#  --atari_exp_id=$exp_id \
#  --dmc_xlim 0 5e6 --dmc_bins 1e5 \
#  --atari_xlim 0 2e7 --atari_bins 1e6 \
#  --size 3.0 2.5 --cols 5 \
#  --atari_tasks atari_boxing atari_freeway atari_pong  atari_tennis \
#  --fig_name transdreamer-atari-chang


#python3 plotting_dmc_atari.py --indir ./logdir --outdir ./plots --xaxis step --yaxis test/return \
#  --xlabel 'Environment Steps' --ylabel 'Episode Return' \
#  --dmc_exp_id=$exp_id \
#  --atari_exp_id=$exp_id \
#  --dmc_xlim 0 5e6 --dmc_bins 1e5 \
#  --atari_xlim 0 2e7 --atari_bins 1e6 \
#  --size 3.0 2.5 --cols 5 \
#  --atari_tasks atari_boxing atari_freeway atari_pong  atari_krull atari_bank_heist \
#  --fig_name dreamer-test-atari

