#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    //Prompt user for input
    string tInput = get_string("Text: ");

    //Loops through the string and checks whether the character
    //is a letter, white space or punctuation character
    float w = 1;
    float l = 0;
    float s = 0;
    int i = 0;
    while (tInput[i] != '\0')
    {
        char cInput = tInput[i];

        switch (cInput)
        {
            case 32:
                w++;
                break;
            case 46:
                s++;
                break;
            case 63:
                s++;
                break;
            case 33:
                s++;
                break;
            default:
                if (isalpha(cInput))
                {
                    l++;
                }
        }
        i++;
    }
    //Calculates L
    float L = l / w * 100;

    //Calculates S
    float S = s / w * 100;

    //Calculates index
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    //Checks index and outputs the corresponding output
    if (index <= 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else {
        switch (index)
        {
            case 2:
                printf("Grade 2\n");
                break;
            case 3:
                printf("Grade 3\n");
                break;
            case 4:
                printf("Grade 4\n");
                break;
            case 5:
                printf("Grade 5\n");
                break;
            case 6:
                printf("Grade 6\n");
                break;
            case 7:
                printf("Grade 7\n");
                break;
            case 8:
                printf("Grade 8\n");
                break;
            case 9:
                printf("Grade 9\n");
                break;
            case 10:
                printf("Grade 10\n");
                break;
            case 11:
                printf("Grade 11\n");
                break;
            case 12:
                printf("Grade 12\n");
                break;
            case 13:
                printf("Grade 13\n");
                break;
            case 14:
                printf("Grade 14\n");
                break;
            case 15:
                printf("Grade 15\n");
                break;
        }
    }
}