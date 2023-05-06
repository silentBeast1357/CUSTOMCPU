# imports sys for argv variable
import sys 

# reads file. Returns 1 if file failed to be read
def readFile(name):
    with open(name,"r") as file:
        if not file.readable:
            return 1
        return file.read()


# lexer class
# needed to seperate the code into parts
class Lexer:
    # Stored text
    text = None

    # stores lines
    lines = []

    # stored parts
    parts = []
    # current part to be appended to parts
    part = ""
    # index of text
    index = 0
    # symbols
    symbols = ","
    
    # special modifiers
    inCmt = False

    # constructor. Takes code as argument 
    def __init__(self, text):
        self.text = text
    
    def appLine(self):
        for part in self.parts:
            if part[0] == "'" and part[-1] == "'" and len(part) != 3:
                print("Char cannot have more than one letter")
                exit()

        if self.parts:
            self.lines.append(self.parts) 
            self.parts = []
    
    # Function to start lexer
    def start(self):
        while self.index < len(self.text):
            self.process()
        
        self.appPart()
        self.appLine()
        return self.lines
    
    # processes individual characters
    def process(self):
        # grabs the char
        char = self.text[self.index]

        # checks if char is in a comment
        if self.inCmt:
            # checks if the char is a \n. Exits out of the comment if so.
            if char == "\n":
                self.inCmt = False
                self.appPart()
                self.appLine()
        elif char == "\n":
            self.appPart()
            self.appLine()
        # Checks if the character is a ;. Enters into comment if so.
        elif char == ";":
            self.inCmt = True
        elif char == ":":
            self.appPart()
            self.part = ":"
            self.appPart()
            self.appLine()
        # checks if the character is a common seperator. appends part if so.
        elif char in " \t\n":
            self.appPart()
        # checks if the character is a symbol. Appends part and then appends the symbol if so
        elif char in self.symbols:
            self.appPart()
            self.parts.append(char)
        # if all the questions above were false the char is added to part
        else:
            self.part += char
        
        # increments index by 1
        self.proceed()
    
    # increments index by 1
    def proceed(self):
        self.index += 1
    
    # appends part
    def appPart(self):
        # checks if part has content
        if self.part:
            self.parts.append(self.part)
            self.part = ""

registerList = ["ax","bx","cx","dx","ex","fx","gx","hx","ix","jx","lx","lo","ds","sp"]

labels = []

class Label:
    def __init__(self,name) -> None:
        self.name = name
        self.validate()
    def validate(self):
        if len(self.name) != 2:
            print("label cant be broken")
            exit()
        if self.name[0] in registerList:
            print("name cant be a register")
    def getOutput(self):
        return f"{self.name[0]}:\n"


class Instruction:
    output = ""
    instruction = []
    def __init__(self,instruction):
        self.instruction = instruction

    def seta0(self,value):
        self.output += str(value) + "\n"
    
    def isa0(self,value):
        return value.isdigit() or (value[0] == "\'" and value[2] == "\'") or value in labels

class Instruction2v(Instruction):
    def validate(self):
        if len(self.instruction) != 4:
            print("Error: wrong instruction format")
            exit()

        if self.instruction[2] != ",":
            print(", is missing")
            exit()

        r1 = self.instruction[1]
        r2 = self.instruction[3]

        r1p = self.instruction[1][0] == "*"
        r2p = self.instruction[3][0] == "*"
        if r1p : r1 = r1[1:]
        if r2p : r2 = r2[1:]

        if not (r1 in registerList or r1 in labels or (r1.isdigit() and r1p)):
            print("Value is not a register or label")
            exit() 
        if not (r1 in registerList or r1 in labels or r1.isdigit()):
            print("Value is not a register, label or a number")
            exit()

class Instruction1v(Instruction):
    def validate(self):
        if len(self.instruction) != 2:
            print("Error: wrong instruction format")
            exit()
        
        v = self.instruction[1]

        if v[0] == "*":
            v = v[1:]
        
        if v not in registerList and v not in labels and not v.isdigit:
            print("Value is not a register, label or a number")
            exit()

class Instruction2v2(Instruction2v):
    name = ""
    def getOutput(self):
        self.validate()
        
        r1 = self.instruction[1]
        r2 = self.instruction[3]
        r1p = r1[0] == "*"
        r2p = r2[0] == "*"
        r1r = r1
        r2r = r2

        if r1p:
            r1r = r1[1:]
        if r2p:
            r2r = r2[1:]
        
        if self.isa0(r2r):
            self.seta0(r2r)

            r2 = ""

            if r2p : r2 = "*"
            r2 += "a0"
        
        self.output += f"{self.name} {r1}, {r2}\n"
        return self.output

class Instruction1v2(Instruction1v):
    name = ""

    def getOutput(self):
        r1 = self.instruction[1]
        r1p = self.instruction[1] == "*"
        r1r = r1 

        if r1p : r1r = r1[1:]

        if self.isa0(r1r):
            self.seta0(r1r)

            r1 = ""
            if r1p : r1 = "*"
            r1 += "a0"
        
        self.output += f"{self.name} {r1}\n"
        return self.output

class add(Instruction2v2):
    name = "add"
class sub(Instruction2v2):
    name = "sub"
class mul(Instruction1v2):
    name = "mul"
class div(Instruction1v2):
    name = "div"
class push(Instruction1v2):
    name = "push"
class pop(Instruction1v2):
    name = "pop"

class ret:
    def __init__(self, parts) : self.parts = parts

    def getOutput(self):
        if len(self.parts) != 1:
            print("Error, too many opperands")
            exit()
        
        return "ret\n"

class db:
    output = ""
    instruction = []
    def __init__(self, instruction):
        self.instruction = instruction
    
    values = []

    def validate(self):
        values = self.instruction[1:]

        index = 1
        while index < len(values):
            if values[index] != ",":
                print("Missing ,")
                exit()
            index += 2
        
        index = 0
        while index < len(values):
            value = values[index]
            if value.isdigit():
                self.values.append(value)
            elif value[0] == '\'' and value[2] == '\'':
                self.values.append(str(ord(value[1])))
            else:
                print("Unknown part found")
                exit()
            index += 2
    def getOutput(self):
        self.validate()
        for num in self.values:
            self.output += num + "\n"
        self.values.clear()
        return self.output

class jmp(Instruction1v):
    def __init__(self, instruction):
        super().__init__(instruction) 
    
    def getOutput(self):
        location = self.instruction[1]
        self.validate()

        if self.isa0(location):
            self.seta0(location)
            location = "a0"
        if self.isa0(location[1:]) and location[0] == "*":
            self.seta0(location[1:])
            location = "*a0"

        self.output += f"mov ds, {location}\njmp\n"
        return self.output
class jz(Instruction1v):
    def __init__(self, instruction):
        super().__init__(instruction) 
    
    def getOutput(self):
        location = self.instruction[1]
        self.validate()

        if self.isa0(location):
            self.seta0(location)
            location = "a0"
        if self.isa0(location[1:]) and location[0] == "*":
            self.seta0(location[1:])
            location = "*a0"

        self.output += f"mov ds, {location}\njz\n"
        return self.output
class jnz(Instruction1v):
    def __init__(self, instruction):
        super().__init__(instruction) 
    
    def getOutput(self):
        location = self.instruction[1]
        self.validate()

        if self.isa0(location):
            self.seta0(location)
            location = "a0"
        if self.isa0(location[1:]) and location[0] == "*":
            self.seta0(location[1:])
            location = "*a0"

        self.output += f"mov ds, {location}\njnz\n"
        return self.output

class call(Instruction1v):
    def __init__(self, instruction):
        super().__init__(instruction) 
    
    def getOutput(self):
        location = self.instruction[1]
        self.validate()

        if self.isa0(location):
            self.seta0(location)
            location = "a0"
        if self.isa0(location[1:]) and location[0] == "*":
            self.seta0(location[1:])
            location = "*a0"

        self.output += f"mov ds, {location}\ncall\n"
        return self.output
class OR(Instruction2v2):
    name = "or"
class INT:
    instruction = []
    def __init__(self, instruction):
        self.instruction = instruction
    
    def validate(self):
        if len(self.instruction) != 2:
            print("wrong instruction format")
            exit()
        
        if not self.instruction[1].isdigit():
            print("Int must get a number as a value not a register")
            exit()
    
    def getOutput(self):
        self.validate()
        return f"int {self.instruction[1]}\n"
class mov(Instruction):
    def __init__(self, instruction):
        super().__init__(instruction)
    def validate(self):
        if len(self.instruction) != 4:
            print("wrong instruction format")
            exit()
        
        if self.instruction[2] != ",":
            print(", is missing")
            exit()
        
        r1 = self.instruction[1]
        r2 = self.instruction[3]
        r1p = r1[0] == "*"
        r2p = r2[0] == "*"

        r1r, r2r = r1, r2

        if r1p: r1r = r1r[1:]
        if r2p: r2r = r2r[1:]

        if r1p:
            if r1r not in registerList and r1r not in labels and not r1r.isdigit():
                print("value is not valid")
                exit()
        else:
            if r1r not in registerList:
                print("value must be a register")
                exit()
        
        if r2r not in registerList and r2r not in labels and not r2r.isdigit() and not (r2r[0] == "'" and r2r[-1] == "'"):
            print(f"value {r2r} is not valid")
            exit()

        
    def getOutput(self):
        self.validate()
        r1 = self.instruction[1]
        r2 = self.instruction[3]

        if self.isa0(r2):
            self.seta0(r2) 
            r2 = "a0"
        elif r2[0] == "*" and self.isa0(r2[1:]):
            self.seta0(r2[1:])
            r2 = "*a0"
        
        self.output += f"mov {r1}, {r2}\n"
        return self.output

class IF(Instruction):
    def __init__(self, instruction):
        super().__init__(instruction)
    
    comparisions = {
        "e":"je",
        "ne":"jne",
        "g":"jg",
        "ge":"jge",
        "l":"jl",
        "le":"jle"
    }
    
    def validate(self):
        if len(self.instruction) != 6:
            print("Invalid format")
            exit()
        if self.instruction[1] not in registerList:
            print(f"{self.instruction[1]} is not a register.")
            exit()

        if self.instruction[2] not in list(self.comparisions):
            print(f"Invalid comparision {self.instruction[2]}")
            exit()
        
        if self.instruction[4] != "jmp":
            print("Missing keyword \"jmp\".")
            exit()
        
        if self.instruction[3] not in registerList and not self.isa0(self.instruction[3][1:] if self.instruction[3][0] == "*" else self.instruction[3]):
            print(f"{self.instruction[3]} is not valid")
            exit()
    
    def getOutput(self):
        self.validate()

        r1 = self.instruction[1]
        r2 = self.instruction[3]
        location = self.instruction[5]

        r2p = r2[0] == "*" 
        locationp = location[0] == "*"

        r2r = r2[1:] if r2p else r2
        locationr = location[1:] if locationp else location

        if self.isa0(locationr):
            self.seta0(locationr)
            location = "*a0" if locationp else "a0"
        self.output += f"mov ds, {location}\n"

        if self.isa0(r2r):
            self.seta0(r2r)
            r2 = "*a0" if r2p else "a0"
        self.output += f"{self.comparisions[self.instruction[2]]} {r1}, {r2}\n"
        return self.output
class xor(Instruction2v2):
    name = "xor"
class nor(Instruction2v2):
    name = "nor"
class AND(Instruction2v2):
    name = "and"
class nand(Instruction2v2):
    name = "nand"
class lshft(Instruction2v2):
    name = "<<"
class rshft(Instruction2v2):
    name = ">>"
# Token seperator class
# needed to sort the parts into commands
class TokenSeperator:

    # list of tokens
    tokenList = []

    # list of parts
    lines = [] 

    # index
    index = 0

    # increases index by given number
    def proceed(self):
        self.index += 1 
    
    # gets part by index or given number
    def getPart(self):
        return self.lines[self.index]

    # constructor
    def __init__(self, parts):
        self.lines = parts
    
    # Processes the line
    def process(self):
        parts = self.getPart()

        if len(parts) == 2:
            if parts[1] == ":":
                self.tokenList.append(Label(parts))
                self.proceed()
                return

        if parts[0] == "mov":
            self.tokenList.append(mov(parts))
        elif parts[0] == "db":
            self.tokenList.append(db(parts))
        elif parts[0] == "int":
            self.tokenList.append(INT(parts))
        elif parts[0] == "jmp":
            self.tokenList.append(jmp(parts))
        elif parts[0] == "add":
            self.tokenList.append(add(parts))
        elif parts[0] == "sub":
            self.tokenList.append(sub(parts))
        elif parts[0] == "pop":
            self.tokenList.append(pop(parts))
        elif parts[0] == "push":
            self.tokenList.append(push(parts))
        elif parts[0] == "call":
            self.tokenList.append(call(parts))
        elif parts[0] == "ret":
            self.tokenList.append(ret(parts))
        elif parts[0] == "or":
            self.tokenList.append(OR(parts))
        elif parts[0] == "jz":
            self.tokenList.append(jz(parts))
        elif parts[0] == "jnz":
            self.tokenList.append(jnz(parts))
        elif parts[0] == "if":
            self.tokenList.append(IF(parts))
        elif parts[0] == "xor":
            self.tokenList.append(xor(parts))
        elif parts[0] == "nor":
            self.tokenList.append(nor(parts))
        elif parts[0] == "and":
            self.tokenList.append(AND(parts))
        elif parts[0] == "nand":
            self.tokenList.append(nand(parts))
        elif parts[0] == "<<":
            self.tokenList.append(lshft(parts))
        elif parts[0] == ">>":
            self.tokenList.append(rshft(parts))
        elif parts[0] == "mul":
            self.tokenList.append(mul(parts))
        elif parts[0] == "div":
            self.tokenList.append(div(parts))

        self.proceed()

    
    # the function the start the seperator
    def start(self):
        for line in self.lines:
            if len(line) == 2:
                if line[1] == ":":
                    label = Label(line)
                    labels.append(label.name[0])
        while self.index < len(self.lines):
            self.process()
        return self.tokenList
def main(argc, argv):
    # checks if argc is 2. Returns 1 if not
    if argc != 2:
        print("Invalid arguments")
        return 1
    
    # reads file
    code = readFile(argv[1])
    # returns 1 if failed to read file
    if code == 1:
        print("Failed to open file")
        return 1
    
    # creates lexer object
    lexer = Lexer(code)

    # runs lexer and stores output
    parts = lexer.start()

    # creates tokenSeperator object 
    tokenSeperator = TokenSeperator(parts);

    # starts seperator and stores the output
    tokens = tokenSeperator.start()
    output = ""

    for token in tokens:
        output += token.getOutput()
    
    with open("assembly.ch","w") as file:
        file.write(output)

    return 0;

# runs main function
if __name__ == "__main__":
    # provides argc and argv from sys
    main(len(sys.argv),sys.argv)