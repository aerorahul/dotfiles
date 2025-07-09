#!/bin/sh --login

datestr=`date +"%Y%m%d"`

[[ -d $HOME/.git ]] && mv $HOME/.git $HOME/.git-$datestr
cp -R git $HOME/.git

files="
gitconfig
"
for file in $files; do
  [[ -f $HOME/.$file ]] && mv $HOME/.$file $HOME/.$file-$datestr
	cp $file $HOME/.$file
done

exit 0
