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

    # constructor. Takes code as argument 
    def __init__(self, text):
        self.text = text
    
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

# runs main function
if __name__ == "__main__":
    # provides argc and argv from sys
    main(len(sys.argv),sys.argv)