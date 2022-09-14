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
    print("INVALIDS")
    exit()

ccStart = f"{input[0]} + {input[1]}"
ccStartAE = ["34", "37"]
ccStartVISA = ["4"]
ccStartMC = ["51", "52", "53", "54", "55"]

if lengthInput == 15:

    if ccStart in ccStartAE:
        print("AMEX")

    else:
        print("INVALID")

elif lengthInput == 13:

    if ccStart[0] in ccStartVISA:
        print("VISA")

    else:
        print("INVALID")

elif lengthInput == 16:

    if ccStart in ccStartMC:
        print("AMEX")

    elif ccStart[0] in ccStartVISA:
        print("VISA")

    else:
        print("INVALID")
else:
    print("INVALID")