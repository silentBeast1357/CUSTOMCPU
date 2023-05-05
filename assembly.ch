main:
0
mov ax, a0
loop:
int 2
1
add ax, a0
mov bx, ax
10
mov ax, a0
int 1
mov ax, bx
loop
mov ds, a0
jmp