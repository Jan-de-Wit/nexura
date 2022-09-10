from cs50 import get_int

# Asks the user for the height until a value between 1 and 8 has been given
while True:
    # Prompts the user for input
    height = get_int("Height: ")

    # Checks if the user has inputted a value between 1 and 8
    if height >= 1 and height <= 8:
        break

# Loops height times
for i in range(1, height + 1):
    # Prints height - i whitespaces
    print(" " * (height - i), end="")

    # Prints i hashes
    print("#" * i, end="")

    # Prints 2 whitespaces
    print("  ", end="")

    # Prints i hashes
    print("#" * i, end="")

    # Prints a new line
    print()