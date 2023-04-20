import sys

class Lexer:
    rawCode = None
    index = 0
    codeParts = []
    part = ""
    def __init__(self,rawCode) -> None:
        self.rawCode = rawCode

    def getPart(self) -> None:
        self.proceed()

    def proceed(self) -> None:
        self.index += 1
    
    def start(self)-> None:
        while self.index < len(self.rawCode):
            self.getPart()




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

if __name__ == "__main__":
    main()