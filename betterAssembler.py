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

    # stored parts
    parts = []
    # current part to be appended to parts
    part = ""
    # index of text
    index = 0
    # symbols
    symbols = ":,"
    
    # special modifiers
    inCmt = False

    # constructor. Takes code as argument 
    def __init__(self, text):
        self.text = text
    
    # Function to start lexer
    def start(self):
        while self.index < len(self.text):
            self.process()
        
        self.appPart()
        print(self.parts)
        return self.parts
    
    # processes individual characters
    def process(self):
        # grabs the char
        char = self.text[self.index]

        # checks if char is in a comment
        if self.inCmt:
            # checks if the char is a \n. Exits out of the comment if so.
            if char == "\n":
                self.inCmt = False
        # Checks if the character is a ;. Enters into comment if so.
        elif char == ";":
            self.inCmt = True
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
    
    # created lexer object
    lexer = Lexer(code)

    # gets parts
    parts = lexer.start()

# runs main function
if __name__ == "__main__":
    # provides argc and argv from sys
    main(len(sys.argv),sys.argv)