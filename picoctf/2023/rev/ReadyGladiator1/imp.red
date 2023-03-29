;redcode
;name Imp Ex
;assert 1
mov 1, 1
start   add.ab  #4, bmb
        mov.i   bmb, @bmb
        jmp     start
bmb     dat     #0, #0
end
