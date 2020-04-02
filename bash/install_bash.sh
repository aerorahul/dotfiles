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
url="https://github.com/git/git/blob/master/contrib/completion"
files="
git-prompt.sh
git-completion.bash
"

for file in $files; do
  [[ -f $HOME/.$file ]] && mv $HOME/.$file $HOME/.$file-$datestr
	wget $url/$file $HOME/.$file
done
exit 0
