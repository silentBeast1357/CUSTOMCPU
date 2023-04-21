import sys

class Instruction:
    def __init__(self, type) -> None:
        self.type = type

class VariableIns(Instruction):
    def __init__(self, type, varType, varName, varValue) -> None:
        super().__init__(type)
        self.varType,self.varName,self.varValue = varType, varName, varValue

class Lexer:
    # Variables
    rawCode = None
    index = 0
    codeParts = []
    part = ""
    symbols = "+-*/=,:;{}()[]"
    inStr = False
    
    # Init function
    def __init__(self,rawCode) -> None:
        self.rawCode = rawCode

    # loop to get code parts
    def getPart(self) -> None:
        # Creates a currentChar variable for less typing
        currentChar = self.rawCode[self.index]
        
        # Checks if the currentChar is in a string 
        if self.inStr:
            # checks if the char is a \
            if currentChar == "\\":
                # gets the next char
                nextChar = self.rawCode[self.index+1]

                # gets special characters
                if nextChar in "\"\'":
                    self.part += nextChar
                elif nextChar == "\\":
                    self.part += nextChar
                else:
                    self.proceed()
                    return
                self.proceed()
            # if current character is a "
            elif currentChar in "\'\"":
                # exits string
                self.part += currentChar
                self.appendPart()
                self.inStr = False
            # adds the current char if the char is not a "
            else : self.part += currentChar
        # checks if char is a "
        elif currentChar in "\"\'":
            # Enters string
            if self.part:
                self.appendPart()
            self.inStr = True
            self.part += currentChar
        # checks if char is a rigged char
        elif currentChar in " \t\n":
            if self.part:
                self.appendPart()
        # checks if char is a symbol
        elif currentChar in self.symbols:
            if self.part:
                self.appendPart()
            self.codeParts.append(currentChar)
        # adds the other characters
        else:
            self.part += currentChar
        # proceeds
        self.proceed()

    # increases the value of index by 1
    def proceed(self) -> None:
        self.index += 1
    # appends part to codeParts and clears part
    def appendPart(self) -> None:
        self.codeParts.append(self.part)
        self.part = ""
    
    # starts the process when called
    def start(self)-> None:
        # Loop for getting parts
        while self.index < len(self.rawCode):
            self.getPart()
        
        if self.inStr:
            print("Never exited out of string. Failed to compile.")
            exit()
        if self.part:
            self.appendPart()
        
        print(self.codeParts)




# Main function
def main() -> int:
    # Checks if args were gived
    if len(sys.argv) != 2:
        print("No file provided")
        return 0

    # Reads file
    fileName = sys.argv[1]
    with open(fileName,"r") as file:
        if file.readable:
            codeRaw = file.read()
    
    # Creats a lexer object and starts it
    lexer = Lexer(codeRaw)
    lexer.start()

if __name__ == "__main__":
    main()