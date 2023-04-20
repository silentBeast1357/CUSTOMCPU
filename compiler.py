import sys

class Lexer:

    # Variables
    rawCode = None
    index = 0
    codeParts = []
    part = ""
    symbols = "+-*/=,:;\{\}()[]"
    
    # Init function
    def __init__(self,rawCode) -> None:
        self.rawCode = rawCode

    # loop to get code parts
    def getPart(self) -> None:
        # creates a currentChar variable for less typing
        currentChar = self.rawCode[self.index]
        # checks if char is a rigged char
        if currentChar in " \t\n":
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