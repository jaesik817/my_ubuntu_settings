syntax on

" display
set number
set ruler

" tab setteings
set shiftwidth=4
set tabstop=4
set softtabstop=4
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
let g:pymode_folding=0
let g:pymode_lint_ignore = "E501,E701,C901"
let g:pymode_rope_lookup_project = 0

call plug#begin('~/.vim/vim/plugged')
Plug 'python-mode/python-mode'
Plug 'ervandew/supertab'
Plug 'heavenshell/vim-pydocstring'
call plug#end()

" remember the last position
au BufReadPost *
\ if line("'\"") > 0 && line("'\"") <= line("$") |
\ exe "norm g`\"" |
\ endif

