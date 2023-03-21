import sys

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
        instructions.append(instruction)

    print(instructions)



if __name__ == "__main__":
    main()