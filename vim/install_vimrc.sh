#!/bin/sh --login

datestr=`date +"%Y%m%d"`

[[ -f $HOME/.vimrc ]] && mv $HOME/.vimrc $HOME.vimrc-$datestr
cp vimrc $HOME/.vimrc

cd ${HOME}

mkdir -p ${HOME}/.vim/autoload
cd ${HOME}/.vim/autoload

# Use of plugins requires plug.vim; get the latest version
if [ -f plug.vim ]; then
    echo "${HOME}/.vim/plug.vim exists, OVERWRITE!"
    cp plug.vim plug.vim-$datestr
fi

if [[ "${OSTYPE}" == "msys" ]]; then
  iwr -useb https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim | \
    ni $HOME/vimfiles/autoload/plug.vim -Force
else
  # Some HPC's do not allow curl; use the clone instead
  #curl -fLo plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
  git clone https://github.com/junegunn/vim-plug.git
  cp -R vim-plug/plug.vim $HOME/.vim/autoload/
  rm -rf vim-plug
fi

# List all the plugins to be used:
plugins="
flazz/vim-colorschemes
vim-airline/vim-airline
vim-airline/vim-airline-themes
tmhedberg/matchit
ntpeters/vim-better-whitespace
gerw/vim-HiLinkTrace
vim-scripts/visSum.vim
will133/vim-dirdiff
mhinz/vim-signify
scrooloose/syntastic
scrooloose/nerdtree
ervandew/supertab
airblade/vim-gitgutter
Xuyuanp/nerdtree-git-plugin
editorconfig/editorconfig-vim
jiangmiao/auto-pairs
tpope/vim-surround
tpope/vim-fugitive
tpope/vim-repeat
tpope/vim-rsi
vim-latex/vim-latex
ryanoasis/vim-devicons
tc50cal/vim-terminal
"

# Location of plugins
mkdir -p ${HOME}/.vim/plugged
cd ${HOME}/.vim/plugged

# Clone plugins from GitHub.com
for plugin in $plugins; do
    git clone https://github.com/$plugin.git
done

updatescr="${HOME}/.vim/update_vimplugins.sh"
[[ -f $updatescr ]] && rm -f $updatescr
touch $updatescr
cat >> $updatescr << EOF
#!/bin/sh --login

cd \${HOME}/.vim/plugged
cwd=\$(pwd)

for i in \$(ls -1); do
    echo "Updating ... \$i"
    cd \$i
    git pull
    cd \$cwd
    echo
done
EOF
chmod +x $updatescr

# Install/Enable plugins
vim -c ":PlugInstall" -c ":q" -c ":q"

exit 0
