# Initial installation
apt-get update
#apt -y install screen
#cp bashrc ~/.bashrc

# vim
curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
#cp viminfo ~/.viminfo
cp vimrc ~/.vimrc
cp -R vim ~/.vim

# tmux
sudo apt-get -y install tmux
cp tmux.conf ~/.tmux.conf

# Git initial Config
git config --global user.name "Jaesik Yoon"
git config --global user.email jaesik.yoon.kr@gmail.com
