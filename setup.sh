# Initial installation
apt update
apt -y install screen

# vim
cp vimrc ~/.vimrc
cp -r vim ~/.vim

# zsh
apt install zsh
wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh
mv ~/.zshrc ~/.zshrc.bak
cp zshrc ~/.zshrc

# Git initial Config
git config --global user.name "Jaesik Yoon"
git config --global user.email jaesik817@gmail.com
