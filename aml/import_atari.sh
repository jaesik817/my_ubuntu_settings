pip install atari-py
wget http://www.atarimania.com/roms/Roms.rar
unrar x Roms.rar
unzip ROMS.zip
python -m atari_py.import_roms ROMS
rm -rf Roms.rar ROMS.zip ROMS 'HC ROMS.zip' 'HC ROMS'
