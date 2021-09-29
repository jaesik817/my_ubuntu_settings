conda_dir=/common/home/jy651/miniconda3
echo 'Remove conda packages'
rm -rf $conda_dir/pkgs/*
echo 'Remove pip cache'
rm -rf .cache/pip/http/*
