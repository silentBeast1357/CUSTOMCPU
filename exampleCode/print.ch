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
    0

stackEnd
mov sp,a0
main
mov ds,a0
jmp

data:
    string:
        'H'
        'e'
        'l'
        'l'
        'o'
        0

print:
    push ax
    push bx
    push cx
    push dx
    push ds

    mov cx,ax
    0
    mov bx,a0
    1
    mov dx,a0
print_loop:
    mov ax,*cx

    print_end
    mov ds,a0
    je ax,bx

    int 1
    add cx,dx
    print_loop
    mov ds,a0
    jmp
print_end:
    pop ds
    pop dx
    pop cx
    pop bx
    pop ax
    ret
    

main:
    string
    mov ax,a0
    print
    mov ds,a0
    call

    int 60