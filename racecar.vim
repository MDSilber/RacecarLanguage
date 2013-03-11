" Vim syntax file
" Language: Racecar
" Maintaner: Sam Kohn
" Latest Revision: 10 March 2013

if exists("b.current_syntax")
  finish
endif

" comments
syn match rcLineComment ":).*$"
syn region rcComment start=":-(" end=":-)"

" code blocks
syn region codeBlock start="{" end="}" contains=rcLineComment,rcComment,ctrlFlow,carManip,directions,types,rcString,rcNumber


" control flow and assignment
" make, using, and, if, else, repeat, set, to
syn keyword ctrlFlow make using and if else repeat set to is not

" car manipulation
" steer, drive, can move, get car position
syn keyword carManip steer drive
syn match carManip "\<can move\>"
syn match carManip "\<get car position\>"

" directions
" forward, forwards, backward, backwards, left, right, straight
syn keyword directions forward forwards backward backwards left right straight

" types
" word, number
syn match types "\<word\>"
syn match types "\<number\>"

" constants
" strings, numbers
syn match rcString "\".\{-}\"" " very simple, no option to escape quotes in string
syn match rcNumber "-\?\d*\.\?\d\+" "int, or float with decimal part (0.5)
syn match rcNumber "-\?\d\+\.\?" "int, or float with no decimal part (5.)


let b:current_syntax = "racecar"

hi def link rcComment Comment
hi def link rcLineComment Comment
hi def link ctrlFlow Statement
hi def link carManip Special
hi def link directions Identifier
hi def link types Type
hi def link rcString Constant
hi def link rcNumber Constant
