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
    0
stackEnd:
    0

main
mov ds,a0
jmp

print:
    69
    mov ax,a0
    int 1
    10
    mov ax,a0
    int 1
    ret


main:
    stackEnd
    mov sp,a0

    print
    mov ds,a0
    call

    int 60