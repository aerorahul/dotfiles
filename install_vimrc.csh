#!/bin/csh -x

cd ~/

mkdir -p ~/.vim/autoload
cd ~/.vim/autoload

if ( -f plug.vim ) then
    echo "~/.vim/plug.vim exists, OVERWRITE!"
    cp plug.vim plug.vim.`date %Y%m%d%M%S`
endif

curl -fLo plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim

# Clone plugins from GitHub.com

mkdir -p ~/.vim/plugged
cd ~/.vim/plugged

set plugins = ( \
    flazz/vim-colorschemes \
    vim-airline/vim-airline \
    vim-airline/vim-airline-themes \
    tmhedberg/matchit \
    npeters/vim-better-whitespace \
    gerw/vim-HiLinkTrace \
    vim-scripts/visSum.vim \
    will133/vim-dirdiff \
    mhinz/vim-signify \
    scrooloose/syntastic \
    ervandew/supertab \
    )

foreach plugin ( $plugins )
    git clone https://github.com/$plugin.git
end

exit 0
