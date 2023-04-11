import sys

def itoh(num,is64=False):
    output = hex(num)[2:].upper()
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

    cl = 0
    for i, instruction in enumerate(instructions):
        if len(instruction) == 2 and instruction[1] == ":":
            labels[instruction[0]] = cl 
        else:
            cl += 1
    for i,instruction in enumerate(instructions):
        if len(instruction) == 1 and instruction[0] in labels:
            instructions[i][0] = str(labels[instruction[0]])

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
        "lo":13,
        "ds":14,
        "sp":15
    }

    output = ""

    for i, instruction in enumerate(instructions):
        first = str(instruction[0])
        if len(first) == 3:
            if first[0] in "\'\"" and first[2] in "\'\"":
                instructions[i] = [str(ord(first[1]))]

    for instruction in instructions:
        if instruction[0] == "mov":
            if instruction[2] != ",":
                print("invalid command. \',\' not present")
                return 1
            r1p = False
            r2p = False
            r1 = 0 
            r2 = 0

            if instruction[1][0] == '*':
                r1p = True
                r1 = registers[instruction[1][1:]]
            else:
                r1 = registers[instruction[1]]
            if instruction[3][0] == '*':
                r2p = True
                r2 = registers[instruction[3][1:]]
            else:
                r2 = registers[instruction[3]]

            cins = htoi("1000000000000000")
            cins += htoi(str(int(r1p))+ itoh(r1)+"00") + htoi(str(int(r2p))+ itoh(r2))
            output += itoh(cins,True) + "\n"
        elif instruction[0] == "int":
            output += "F"+itoh(int(instruction[1]),True)[1:] + "\n"
        elif instruction[0] == "add":
            cins = htoi("2000000000000000")
            cins += registers[instruction[1]]*16 + registers[instruction[3]]
            if instruction[2] != ",":
                print("invalid command. \',\' not present")
                return 1
            output += itoh(cins,True) + "\n"
        elif instruction[0] == "sub":
            cins = htoi("2100000000000000")
            cins += registers[instruction[1]]*16 + registers[instruction[3]]
            if instruction[2] != ",":
                print("invalid command. \',\' not present")
                return 1
            output += itoh(cins,True) + "\n"
        elif instruction[0] == "mul":
            cins = htoi("2200000000000000")
            cins += registers[instruction[1]]
            output += itoh(cins,True) + "\n"
        elif instruction[0] == "div":
            cins = htoi("2300000000000000")
            cins += registers[instruction[1]]
            output += itoh(cins,True) + "\n"
        elif instruction[0] == "jmp":
            output += "3000000000000000\n"
        elif instruction[0] == "je":
            cins = htoi("3100000000000000")
            cins += registers[instruction[1]]*16 + registers[instruction[3]]
            if instruction[2] != ",":
                print("invalid command. \',\' not present")
                return 1
            output += itoh(cins,True) + "\n"
        elif instruction[0] == "jne":
            cins = htoi("3200000000000000")
            cins += registers[instruction[1]]*16 + registers[instruction[3]]
            if instruction[2] != ",":
                print("invalid command. \',\' not present")
                return 1
            output += itoh(cins,True) + "\n"
        elif instruction[0] == "jl":
            cins = htoi("3300000000000000")
            cins += registers[instruction[1]]*16 + registers[instruction[3]]
            if instruction[2] != ",":
                print("invalid command. \',\' not present")
                return 1
            output += itoh(cins,True) + "\n"
        elif instruction[0] == "jle":
            cins = htoi("3400000000000000")
            cins += registers[instruction[1]]*16 + registers[instruction[3]]
            if instruction[2] != ",":
                print("invalid command. \',\' not present")
                return 1
            output += itoh(cins,True) + "\n"
        elif instruction[0] == "jg":
            cins = htoi("3500000000000000")
            cins += registers[instruction[1]]*16 + registers[instruction[3]]
            if instruction[2] != ",":
                print("invalid command. \',\' not present")
                return 1
            output += itoh(cins,True) + "\n"
        elif instruction[0] == "jge":
            cins = htoi("3600000000000000")
            cins += registers[instruction[1]]*16 + registers[instruction[3]]
            if instruction[2] != ",":
                print("invalid command. \',\' not present")
                return 1
            output += itoh(cins,True) + "\n"
        elif instruction[0] == "call":
            output += "6000000000000001\n"
        elif instruction[0] == "ret":
            output += "6000000000000002\n"
        elif instruction[0] == "push":
            output += "400000000000000" + itoh(registers[instruction[1]]) + "\n"
        elif instruction[0] == "pop":
            output += "500000000000000" + itoh(registers[instruction[1]]) + "\n"
        elif len(instruction) == 1:
            output += itoh(int(instruction[0]),True) + "\n"

    with open("bin","w") as file:
        file.write(output)

if __name__ == "__main__":
    main()