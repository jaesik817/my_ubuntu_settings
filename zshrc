# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
#export ZSH="/cortex/users/jy651/.oh-my-zsh"
export ZSH="/common/home/jy651/.oh-my-zsh"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time oh-my-zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
ZSH_THEME="robbyrussell"

# Set list of themes to pick from when loading at random
# Setting this variable when ZSH_THEME=random will cause zsh to load
# a theme from this variable instead of looking in $ZSH/themes/
# If set to an empty array, this variable will have no effect.
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion.
# Case-sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to automatically update without prompting.
# DISABLE_UPDATE_PROMPT="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line if pasting URLs and other text is messed up.
# DISABLE_MAGIC_FUNCTIONS="true"

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load?
# Standard plugins can be found in $ZSH/plugins/
# Custom plugins may be added to $ZSH_CUSTOM/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(git)

source $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"
#

export CORTEX=/cortex/users/jy651
export COMMON=/common/home/jy651

##############################################################################
# Commands
##############################################################################
# gpus
alias gi='gpustat -cpu'
alias gis='gpustats'

# video-transformer
alias vtcd='cd /cortex/users/jy651/video-transformer/'
alias vtdcd='cd /data/local/jy651/vt/'

# nvae
alias nvcd='cd /cortex/users/jy651/attention_vae/'
alias nvdcd='cd /data/local/jy651/nvae/data/'
alias nvlcd='cd /data/local/jy651/nvae/logs/'

# vdvae
alias vdcd='cd /cortex/users/jy651/attentive_vdvae/'
alias vddcd='cd /data/local/jy651/vdvae/data/'
alias vdlcd='cd /data/local/jy651/vdvae/logs/'

# scalable_agent
alias scd='cd /cortex/users/jy651/scalable_agent/'

# etc
alias dcd='cd /data/local/jy651/'
alias dscd='cd /data/sdb/local/jy651/'
alias hcd='cd ~'
alias whiledocker='while true; do; docker ps -a; sleep 2; done'
alias whilegi='while true; do; gi; sleep 2; done'
alias whilefree='while true; do; free -g; sleep 2; done'
alias ccd='cd /common/users/jy651/'
#alias ccd='cd /cortex/users/jy651/'

# tmux
alias tl='tmux ls'
alias ta='tmux attach-session -t '
alias tk='tmux kill-session -t '

##############################################################################
# Conda
##############################################################################
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/common/home/jy651/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/common/home/jy651/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/common/home/jy651/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/common/home/jy651/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
if [ $(hostname) = "rumelhart.cs.rutgers.edu" ]
then
  conda activate transdreamer-rumelhart
else
  conda activate transdreamer
fi
# <<< conda initialize <<<


export PATH=/cortex/users/jy651/ahnlab_tools:$PATH
export ML_TOOL_PATH=/cortex/users/jy651/ahnlab_tools

export PATH="$COMMON/bin:$COMMON/nvidia-docker/bin:$PATH"
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock

export PATH=/cortex/users/jy651/ddocker:$PATH
export DIST_DOCKER_PATH=/cortex/users/jy651/ddocker

export PATH=/common/home/jy651/bin:/common/home/jy651/.local/bin:$PATH
#export DOCKER_HOST=unix:///run/user/88374/docker.sock
