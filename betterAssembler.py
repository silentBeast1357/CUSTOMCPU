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

        if r1 not in registerList:
            print(f"{r1} is not a valid register")
            exit()
        if r2 not in registerList:
            print(f"{r2} is not a valid register")
            exit()

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
            elif value[0] == '\'' and value[-1] == '\'':
                self.values.append(str(ord(value[1])))
            else:
                print("Unknown part found")
                exit()
            index += 2
    def getOutput(self):
        self.validate()
        for num in self.values:
            self.output += num + "\n"
        return self.output


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

        if r1[0] == "*":
            r1 = r1[1:]
        if r2[0] == "*":
            r2 = r2[1:]
        
        if r1 not in registerList:
            print(f"{r1} is not a valid register")
            exit()
        if r2 not in registerList and not r2.isdigit() and r2 not in labels:
            print(f"{r2} is not a valid register or number")
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

        if parts[0] == "mov":
            self.tokenList.append(mov(parts))
        elif parts[0] == "db":
            self.tokenList.append(db(parts))
        elif parts[0] == "int":
            self.tokenList.append(INT(parts))
        elif parts[1] == ":":
            self.tokenList.append(Label(parts))

        self.proceed()

    
    # the function the start the seperator
    def start(self):
        for line in self.lines:
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
    print(parts)

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