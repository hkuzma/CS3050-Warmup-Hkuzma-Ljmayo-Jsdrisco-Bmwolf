def main():
    quit = False
    while quit != True:
        user_input = input("??")
        user_input = user_input.lower()
        if user_input == "quit":
            quit = True
            break
        if user_input == "help":
            printCommands()
    print("Exiting")


def printCommands():
    pass