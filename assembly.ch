10
mov ax,a0
10
mov bx,a0
end
mov ds,a0
jle ax,bx

int 60

end:
    int 2
    int 60