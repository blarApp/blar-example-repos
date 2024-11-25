from helper1 import greet
from helper2 import farewell

def main():
    # Use functions from helper modules
    greeting = greet()
    goodbye = farewell()

    print(greeting)
    print(goodbye)

if __name__ == "__main__":
    main()
