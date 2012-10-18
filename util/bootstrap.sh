#!/usr/bin/env zsh

DOTFILES=$HOME/.dotfiles
BASE_FILES=( "bash_profile" "bashrc" "profile" "zprofile" "zshrc")
ETC_FILES=("ackrc" "psqlrc" "gemrc" "sqlplus_completions" "tmux.conf" "wgetrc")
GIT_FILES=("gitconfig" "gitignore_global")
VIM_FILES=("vimrc" "gvimrc")

createBaseSymlinks () {
for i in ${BASE_FILES[@]}
do
  if [ -f ~/.${i} ] || [ -h ~/.${i} ]
    then
      printf "Found ~/.${i}... Backing up to ~/.${i}.old\n";
      cp ~/.${i} ~/.${i}.old;
      rm ~/.${i};
  fi
  printf "Creating alias for ${i}\n"
  ln -s ${DOTFILES}/${i} ~/.${i}
done
}

createEtcSymlinks () {
for i in ${ETC_FILES[@]}
do
  if [ -f ~/.${i} ] || [ -h ~/.${i} ]
    then
      printf "Found ~/.${i}... Backing up to ~/.${i}.old\n";
      cp ~/.${i} ~/.${i}.old;
      rm ~/.${i};
  fi
  printf "Creating alias for ${i}\n"
  ln -s ${DOTFILES}/etc/${i} ~/.${i}
done
}

createGitSymlinks () {
for i in ${GIT_FILES[@]}
do
  if [ -f ~/.${i} ] || [ -h ~/.${i} ]
    then
      printf "Found ~/.${i}... Backing up to ~/.${i}.old\n";
      cp ~/.${i} ~/.${i}.old;
      rm ~/.${i};
  fi
  printf "Creating alias for ${i}\n"
  ln -s ${DOTFILES}/git/${i} ~/.${i}
done
}

createVimSymlinks () {
for i in ${VIM_FILES[@]}
do
  if [ -f ~/.${i} ] || [ -h ~/.${i} ]
    then
      printf "Found ~/.${i}... Backing up to ~/.${i}.old\n";
      cp ~/.${i} ~/.${i}.old;
      rm ~/.${i};
  fi
  printf "Creating alias for ${i}\n"
  ln -s ${DOTFILES}/vim/${i} ~/.${i}
done

#Create symlink for vim directory
ln -s $DOTFILES/vim/ ~/.vim
}

createBaseSymlinks
createEtcSymlinks
createGitSymlinks
createVimSymlinks

# Only copy ssh config if it doesn't already exist
[[ -f $HOME/.ssh/config ]] || cp $DOTFILES/etc/ssh_config $HOME/.ssh/config

