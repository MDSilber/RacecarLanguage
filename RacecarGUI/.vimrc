set number
set mouse=a
:imap ^h <BS>
set tw=80

set autoindent

set nocompatible 

set whichwrap+=<,>,h,l,[,]
"highlight comment ctermfg=lightblue
"highlight constant ctermfg=red
:syntax on
map ` :tabnext <CR>

let java_highlight_all=1
let java_highlight_functions="style"
let java_highlight_debug=1
let java_highlight_java_lang_ids=1

autocmd VimEnter * NERDTree
autocmd VimEnter * wincmd p


function! NERDTreeQuit()
	redir => buffersoutput
	silent buffers
	redir END	
      	"                     1BufNo  2Mods.     3File           4LineNo
	let pattern = '^\s*\(\d\+\)\(.....\) "\(.*\)"\s\+line \(\d\+\)$'
	let windowfound = 0

	for bline in split(buffersoutput, "\n")
		let m = matchlist(bline, pattern)
		if (len(m) > 0)
	        	if (m[2] =~ '..a..')
	          	let windowfound = 1
			endif
		endif
	endfor

	if (!windowfound)
	   quitall
	endif

endfunction
autocmd WinEnter * call NERDTreeQuit()
