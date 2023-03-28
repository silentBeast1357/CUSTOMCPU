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

main
mov ds,a0
jmp

print:
    int 2

    push ax
    10
    mov ax,a0
    int 1
    pop ax

    ret

main:
    stackEnd
    mov sp,a0

    1
    mov bx,a0
    100
    mov cx,a0
loop:
    add ax,bx

    print
    mov ds,a0
    call

    end
    mov ds,a0
    je ax,cx
    loop
    mov ds,a0
    jmp
end:
    int 60