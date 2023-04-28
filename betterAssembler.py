import sys 

class Lexer:
    text = None
    def __init__(self, text) -> None:
        self.text = text

def main(argc, argv):
    print("Hello World!")

if __name__ == "__main__":
    main(len(sys.argv),sys.argv)