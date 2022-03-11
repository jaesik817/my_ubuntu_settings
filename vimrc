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
set nofoldenable

" misc
set nu
set autoread
set cc=80

" python
au FileType python set cc=80
highlight ColorColumn   ctermbg=52 guibg=#5f0000

"let g:pymode_indent = v:false

"call plug#begin('~/.vim/vim/plugged')
"Plug 'python-mode/python-mode'
"call plug#end()

" remember the last position
au BufReadPost *
\ if line("'\"") > 0 && line("'\"") <= line("$") |
\ exe "norm g`\"" |
\ endif
