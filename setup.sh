apt update

cp bashrc ~/.bashrc
cp tmux.reset.conf ~/.tmux.reset.conf
cp tmux.2nd.conf ~/.tmux.2nd.conf
cp tmux.conf ~/.tmux.conf
cp viminfo ~/.viminfo
cp vimrc ~/.vimrc
cp zshrc ~/.zshrc

cp -R vim ~/.vim

# Install tmux
apt -y install tmux

# Install zsh
#apt -y install zsh
#apt -y install git-core
#wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh
#rm -rf ~/.zshrc
#cp zshrc ~/.zshrc
#chsh -s `which zsh`
# sudo shutdown -r 0
