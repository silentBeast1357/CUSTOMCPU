stack:
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
stackEnd:
stackEnd
mov sp, a0
1
sub sp, a0
main
mov ds, a0
jmpmain:
loop:
int 2
push ax
10
mov ax, a0
int 1
pop ax
1
add ax, a0
loop
mov ds, a0
jmp