syntax on

" display
set nonumber
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
"set nu
set autoread
    
" python
au FileType python set cc=80
highlight ColorColumn   ctermbg=52 guibg=#5f0000
let g:pymode_folding=0
let g:pymode_lint_ignore = "E501,E701,C901"
let g:pymode_rope_lookup_project = 0

call plug#begin('~/.vim/plugged')
Plug 'python-mode/python-mode'
Plug 'ervandew/supertab'
call plug#end()

" Uncomment the following to have Vim jump to the last position when
" reopening a file
if has("autocmd")
  au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
endif
