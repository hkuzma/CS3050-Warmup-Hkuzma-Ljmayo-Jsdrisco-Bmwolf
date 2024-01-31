def main():
    quit = False
    while quit != True:
        user_input = input("??\n")
        user_input = user_input.lower()
        if user_input == "quit":
            quit = True
            break
        if user_input == "help":
            printCommands()
    print("Exiting")


def printCommands():
    pass

if __name__ == "__main__":
    main()