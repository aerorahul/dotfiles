#!/bin/sh --login

cd ${HOME}

mkdir -p ${HOME}/.vim/autoload
cd ${HOME}/.vim/autoload

# Use of plugins requires plug.vim; get the latest version
if [ -f plug.vim ]; then
    echo "${HOME}/.vim/plug.vim exists, OVERWRITE!"
    cp plug.vim plug.vim.`date %Y%m%d%M%S`
fi
curl -fLo plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim

# List all the plugins to be used:
plugins="
flazz/vim-colorschemes
vim-airline/vim-airline
vim-airline/vim-airline-themes
tmhedberg/matchit
tpope/vim-surround
ntpeters/vim-better-whitespace
gerw/vim-HiLinkTrace
vim-scripts/visSum.vim
will133/vim-dirdiff
mhinz/vim-signify
scrooloose/syntastic
ervandew/supertab
scrooloose/nerdtree
airblade/vim-gitgutter
Xuyuanp/nerdtree-git-plugin
editorconfig/editorconfig-vim
jiangmiao/auto-pairs
ryanoasis/vim-devicons
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

exit 0
