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

exit 0
