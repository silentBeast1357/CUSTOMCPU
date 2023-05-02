loop:
'E'
mov ax, a0
int 1
10
mov ax, a0
int 1
loop
mov ds, a0
jmp