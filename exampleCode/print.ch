stack:
    0
    0
    0
    0
    0
stackEnd:

stackEnd
mov sp,a0
1
sub sp,a0
main
mov ds,a0
jmp

text:
    "H"
    "e"
    "l"
    "l"
    "o"
    10
    0

printStr:
    push ax
    push bx
    push cx

    mov bx,ax
    1
    mov cx,a0

    printStr_loop
    mov ds,a0
printStr_loop:
    mov ax,*bx
    int 1
    or ax,ax
    add bx,cx
    jnz
printStr_end:
    pop cx
    pop bx
    pop ax
    ret

main:
    text
    mov ax,a0
    printStr
    mov ds,a0
    call

    int 60