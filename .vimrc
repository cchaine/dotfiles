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

" Automatically reload files modified outside vim
set autoread

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
colorscheme jellybeans 
let g:lightline = { 'colorscheme' : 'jellybeans' }

" NERDTree configuration
let NERDTreeShowHidden = 1
let NERDTreeMinimalUI = 1
let NERDTreeDirArrows = 1

" Clang-format
autocmd FileType c,cpp,java nnoremap <C-f> :<C-u>ClangFormat<CR>
autocmd FileTYpe c,cpp,java vnoremap <C-f> :ClangFormat<CR>

" jcommenter
" map the commenter:
autocmd FileType java let b:jcommenter_file_author='Clément Chaine (cc.chaine@free.fr)'

map <C-d> :call JCommentWriter()<CR>
imap <C-d> <esc>:call JCommentWriter()<CR>

" Move cursor to the place where inserting comments supposedly should start
autocmd FileType java let b:jcommenter_move_cursor = 1

" Defines whether to move the cursor to the line which has "/**", or the line
" after that (effective only if b:jcommenter_move_cursor is enabled)
autocmd FileType java let b:jcommenter_description_starts_from_first_line = 0

" Start insert mode after calling the commenter. Effective only if 
" b:jcommenter_move_cursor is enabled.
autocmd FileType java let b:jcommenter_autostart_insert_mode = 1

" The number of empty rows (containing only the star) to be added for the 
" description of the method
autocmd FileType java let b:jcommenter_method_description_space = 2

" define whether jcommenter tries to parse and update the existing Doc-comments
" on the item it was executed on. If this feature is disabled, a completely new
" comment-template is written
autocmd FileType java let b:jcommenter_update_comments = 1

" Whether to prepend an empty line before the generated comment, if the
" line just above the comment would otherwise be non-empty.
autocmd FileType java let b:jcommenter_add_empty_line = 1

function! JCommenter_OwnFileComments()
  call append(0, '/*')
  call append(1, ' * File name   : ' . bufname("%"))
  call append(2, ' * authors     : ' . b:jcommenter_file_author)
  call append(3, ' * created     : ' . strftime("%c"))
  call append(4, ' *')
  call append(5, ' */')
  call append(6, '')
endfunction
