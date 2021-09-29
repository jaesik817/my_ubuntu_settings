# Initial installation
#apt-get update


# vim
curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
cp vimrc ~/.vimrc
cp -R vim ~/.vim


# tmux
apt-get install -y tmux
cp tmux.conf ~/.tmux.conf


# Install zsh
sudo apt-get -y install zsh
sudo apt-get -y install git-core
wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh
rm -rf ~/.zshrc
cp zshrc ~/.zshrc
chsh -s `which zsh`


# Git initial Config
git config --global user.name "Jaesik Yoon"
git config --global user.email jaesik.yoon.kr@gmail.com
