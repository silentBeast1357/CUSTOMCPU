import sys

def itoh(num,is64=False):
    n = num
    stack = [] 
    
    while n > 0:
        stack.append(n % 16)
        n /= 16
        n = int(n)
    
    output = ""
    while stack:
        n = stack.pop()

        if n >= 10 and n <= 16:
            n = chr(ord("A")+(n-10))
        else:
            n = str(n)
        
        output += n
    
    if is64:
        tmp = output
        output = ""

        for i in range(16-len(tmp)):
            output += "0"
        output += tmp
    
    return output

def htoi(hex):
    output = 0
    multiplier = 1
    for char in hex[::-1]:
        if ord(char) >= ord("A") and ord(char) <= ord("F"):
            output += (ord(char)-ord("A")+10)*multiplier
        else:
            output += int(char) * multiplier
        multiplier *= 16
    return output


def main():
    if len(sys.argv) != 2:
        print("Error: no file provided")
        return 1

    with open(sys.argv[1],"r") as file:
        if not file.readable:
            print("Error: file not found")
            return 1
        rawCode = file.read()
    
    rawLines = rawCode.split("\n")
    instructions = []
    for line in rawLines:
        lastInstruction = ""
        instruction = []

        for char in line:
            if char == " ":
                if lastInstruction:
                    instruction.append(lastInstruction) 
                    lastInstruction = ""
            elif char in ",:":
                if lastInstruction:
                    instruction.append(lastInstruction)
                    lastInstruction = ""
                instruction.append(char)
            else:
                lastInstruction += char
        
        if lastInstruction:
            instruction.append(lastInstruction)
        if instruction:
            instructions.append(instruction)

    labels = {}

    for i, instruction in enumerate(instructions):
        if len(instruction) == 2 and instruction[1] == ":":
            labels[instruction[0]] = i
    
    registers = {
        "a0":0,
        "ax":1,
        "bx":2,
        "cx":3,
        "dx":4,
        "ex":5,
        "fx":6,
        "gx":7,
        "hx":8,
        "ix":9,
        "jx":10,
        "kx":11,
        "lx":12,
        "mx":13,
        "ds":14,
        "sp":15
    }

    

if __name__ == "__main__":
    main()