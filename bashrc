
# PROMPT

# ALIASES
# cd
alias ..='cd ..'
# ls
alias ls="ls -F"
alias l="ls -lAh"
alias ll="ls -l"
alias la='ls -A'
# git
alias gl='git pull'
alias gp='git push'
alias gpom='git push origin master'
alias gd='git diff'
alias gc='git commit'
alias gca='git commit -a'
alias gco='git checkout'
alias gb='git branch'
alias gs='git status'
alias grm="git status | grep deleted | awk '{print \$3}' | xargs git rm"
alias pull='git pull origin master'

# use .localrc for settings specific to one system
if [ -f ~/.localrc ]; then
  source ~/.localrc
fi

export EDITOR=vim
. ~/.dotfiles/bin/bash_colors.sh

# Add paths
export PATH=$PATH:~/.bin
export PATH=$PATH:~/.dotfiles/bin
