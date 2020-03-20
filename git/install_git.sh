#!/bin/sh --login

datestr=`date %Y%m%d%M%S`

[[ -d $HOME/.git ]] && mv $HOME/.git $HOME/.git-$datestr
cp -R git $HOME/.git

files="
git-clone-init
gitconfig
"
for file in $files; do
  [[ -f $HOME/.$file ]] && mv $HOME/.$file $HOME/.$file-$datestr
	cp $file $HOME/.$file
done

exit 0
