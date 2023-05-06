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
stackEnd:
stackEnd
mov sp, a0
1
sub sp, a0
main
mov ds, a0
jmp
true:
84
114
117
101
10
0
false:
70
97
108
115
101
10
0
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
main:
100
mov ax, a0
success
mov ds, a0
10
jg ax, a0
fail:
false
mov ax, a0
print
mov ds, a0
call
int 60
success:
true
mov ax, a0
print
mov ds, a0
call
int 60
