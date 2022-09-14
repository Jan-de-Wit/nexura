from cs50 import get_string
from sys import exit

while True:
    # Gets user input and reverses the string
    rawInput = get_string("Number: ")

    if rawInput.isdigit() == True:
        break

input = rawInput[::-1]

lengthInput = len(input)

multipliedSum = 0
normalSum = 0
finalSum = 0

# Iterates through every digit in the input
for i in range(lengthInput):
    # Saves value in a temporary variable
    number = int(input[i])

    # Checks if i is even (meaning its the first, third, fifth, etc. digit)
    if i % 2 == 0:
        # Adds number to an array with all numbers
        normalSum += number

    # Checks if i is even (meaning its the second, fourth, sixth, etc. digit)
    else:
        # Multiplies the number by 2
        multiplied = number * 2

        # Seperates the digits of the multiplied value and adds them in an array
        for d in str(multiplied):
            multipliedSum += int(d)

finalSum = normalSum + multipliedSum

if finalSum % 10 != 0:
    print("INVALID")
    exit()

ccStart = f"{rawInput[0]}{rawInput[1]}"

if lengthInput == 15:

    if ccStart == "34" or ccStart == "37":
        print("AMEX")
        exit()
    else:
        print("INVALID")
        exit()
elif lengthInput == 13:

    if ccStart[0] == "4":
        print("VISA")
        exit()
    else:
        print("INVALID")
        exit()
elif lengthInput == 16:
    if int(ccStart) >= 51 and int(ccStart) <= 55:
        print("MASTERCARD")
        exit()
    elif ccStart[0] == "4":
        print("VISA")
        exit()
    else:
        print("INVALID")
        exit()
else:
    print("INVALID")
    exit()