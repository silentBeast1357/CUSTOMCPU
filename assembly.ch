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
jmp
print:
push ax
push cx
mov cx, ax
print_loop:
mov ax, *cx
or ax, ax
print_end
mov ds, a0
jz
int 1
1
add cx, a0
print_loop
mov ds, a0
jmp
print_end:
pop cx
pop ax
ret
text:
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
main:
15
mov bx, a0
text
mov ax, a0
int 3
print
mov ds, a0
call
int 60
