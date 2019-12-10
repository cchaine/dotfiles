set nobackup
set nowb
set noswapfile
set noerrorbells

set hidden
set history=100

set mouse=a

nnoremap <Left> h
nnoremap <Right> l
nnoremap <Up> k
nnoremap <Down> j

" Appearance "
syntax enable

set number
set linespace=12

set title
set noshowmode
set laststatus=2

set background=dark

set showmatch

" File behaviour "
set expandtab
set smarttab
set linebreak

set shiftwidth=2
set tabstop=2

au BufRead,BufNewFile *.ts setfiletype javascript
" Search "
set smartcase
set hlsearch
set incsearch

" Bindings "
map <C-o> :NERDTreeToggle<CR>

" Plugins "

" Install and run vim-plug on first run
if empty(glob('~/.vim/autoload/plug.vim'))
    silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
    \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
    autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif

so ~/.vim/plugins.vim
colorscheme gruvbox
let g:lightline = { 'colorscheme' : 'gruvbox' }

let NERDTreeShowHidden = 1
