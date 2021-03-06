#!/bin/sh --login

datestr=`date +"%Y%m%d"`

files="
bash_profile
bash_aliases
bash_functions
"
for file in $files; do
  [[ -f $HOME/.$file ]] && mv $HOME/.$file $HOME/.$file-$datestr
  cp $file $HOME/.$file
done

# Grab git friendly files for bash from url below
url="https://raw.githubusercontent.com/git/git/master/contrib/completion"
files="
git-completion.bash
"
for file in $files; do
  [[ -f $HOME/.$file ]] && mv $HOME/.$file $HOME/.$file-$datestr
  wget $url/$file && mv $file $HOME/.$file
done

# Grab git prompt for bash
git clone https://github.com/magicmonty/bash-git-prompt $HOME/.bash-git-prompt

exit 0
