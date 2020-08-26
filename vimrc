syntax on

" display
set number
set ruler

" tab setteings
set shiftwidth=2
set tabstop=2
set softtabstop=2
set expandtab
set autoindent

" search
set ignorecase
set smartcase
set incsearch
set hlsearch
set showmatch

" misc
set nu
set autoread

" python
au FileType python set cc=80
highlight ColorColumn   ctermbg=52 guibg=#5f0000

" python mode plugin
call plug#begin('~/.vim/vim/plugged')
Plug 'python-mode/python-mode'
call plug#end()

" remember the last position
au BufReadPost *
\ if line("'\"") > 0 && line("'\"") <= line("$") |
\ exe "norm g`\"" |
\ endif

