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
            //Checks if cInput is a white space
            case 32:
                w++;
                break;
            //Checks if cInput is a period
            case 46:
                s++;
                break;
            case 63:
            //Checks if cInput is a question mark
                s++;
                break;
            case 33:
            //Checks if cInput is an exclamation mark
                s++;
                break;
            default:
            //Checks if cInput is a letter
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
        //Prints corresponding output
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        //Prints corresponding output
        printf("Grade 16+\n");
    }
    else
    {
        //Checks index for index 2-15
        switch (index)
        {
            case 2:
                //Prints corresponding output
                printf("Grade 2\n");
                break;
            case 3:
                //Prints corresponding output
                printf("Grade 3\n");
                break;
            case 4:
                //Prints corresponding output
                printf("Grade 4\n");
                break;
            case 5:
                //Prints corresponding output
                printf("Grade 5\n");
                break;
            case 6:
                //Prints corresponding output
                printf("Grade 6\n");
                break;
            case 7:
                //Prints corresponding output
                printf("Grade 7\n");
                break;
            case 8:
                //Prints corresponding output
                printf("Grade 8\n");
                break;
            case 9:
                //Prints corresponding output
                printf("Grade 9\n");
                break;
            case 10:
                //Prints corresponding output
                printf("Grade 10\n");
                break;
            case 11:
                //Prints corresponding output
                printf("Grade 11\n");
                break;
            case 12:
                //Prints corresponding output
                printf("Grade 12\n");
                break;
            case 13:
                //Prints corresponding output
                printf("Grade 13\n");
                break;
            case 14:
                //Prints corresponding output
                printf("Grade 14\n");
                break;
            case 15:
                //Prints corresponding output
                printf("Grade 15\n");
                break;
        }
    }
}