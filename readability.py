from cs50 import get_string

# Prompts the user for a text
input = get_string("Text: ")

punctuation = [".", "!", "?"]
letterCount = 0
wordCount = 1
sentenceCount = 0

# Iterates through every character in the by the user inputted string
for index in range(len(input)):
    # Assigns the character in the sentence to a temporary variable
    char = input[index]

    # Checks if the character is an alphabetical character
    if char.isalpha() == 1:
        letterCount += 1
    # Checks if the character is whitespace
    elif char.isspace() == 1:
        wordCount += 1
    # Checks if the character is a punctuation character which isn't a comma
    elif char in punctuation:
        sentenceCount += 1

# Gets the average amount of letters per 100 words
avgLpW = letterCount / wordCount * 100

# Gets the average amount of sentences per 100 words
avgSpW = sentenceCount / wordCount * 100

# Calculates what grade the user input is and rounds it
grade = round(0.0588 * avgLpW - 0.296 * avgSpW - 15.8)

# Checks if grade is smaller than 1
if grade < 1:
    print(f"Before Grade 1")

# Checks if grade is larger than 16
elif grade > 16:
    print(f"Grade 16+")

else:
    print(f"Grade: {grade}")