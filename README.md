# dotfiles #
A repository to hold custom dot files e.g. `.cshrc`, `.vimrc`, etc.

## vimrc ##
The use of plugins requires:
* `.vim/autoload/plug.vim` - Enables plugins
* `.vim/plugged` - location of vim-plugins

Download `plug.vim` and put it in `~/.vim/autoload`
* `curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim`

The following plugins are used:
* flazz/vim-colorschemes
* vim-airline/vim-airline
* vim-airline/vim-airline-themes
* tmhedberg/matchit
* npeters/vim-better-whitespace
* gerw/vim-HiLinkTrace
* vim-scripts/visSum.vim
* will133/vim-dirdiff
* mhinz/vim-signify
* scrooloose/syntastic
* ervandew/supertab

These plugins can be cloned from [GitHub](www.github.com)
* `git clone https://github.com/$plugin.git`
