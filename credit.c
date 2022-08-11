#include <stdio.h>
#include <string.h>
#include <cs50.h>

int main()
{
    //Prompts for user input
    long n = get_long("Number: ");

    //Makes an array with the input
    int arr[16];
    char s[17];
    sprintf(s, "%ld", n);
    int leng = strlen(s);
    int i;
    for (i = 0; i < leng; i++)
    {
        arr[i] = s[i] - '0';
    }

    //Some necessary calls for variables and arrays to use in and
    //outside of the for loop
    char nMultAdd[16];
    char nMultTemp[17];
    int lengMA;
    int nAdd = 0;
    //Checks if number is even or odd
    if (i % 2 == 0)
    {
        //Loops through all the numbers
        int j;
        for (j = 0; j < leng; j++)
        {
            //Checks whether counter is even or odd
            if (j % 2 == 0)
            {
                //Multiplies the according number in the array
                int iMult = arr[j] * 2;

                //Converts the multiplied amount into a string
                //and adds it into a larger string
                sprintf(nMultTemp, "%d", iMult);
                strcat(nMultAdd, nMultTemp);
            }
            else
            {
                //Sums up numbers
                nAdd = nAdd + arr[j];
            }
        }
    }
    else
    {
        //Loops through all the numbers
        int j;
        for (j = 0; j < leng; j++)
        {
            //Checks whether counter is even or odd
            if (j % 2 == 0)
            {
                //Sums up numbers
                nAdd = nAdd + arr[j];
            }
            else
            {
                //Multiplies the according number in the array
                int iMult = arr[j] * 2;

                //Converts the multiplied amount into a string
                //and adds it into a larger string
                sprintf(nMultTemp, "%d", iMult);
                strcat(nMultAdd, nMultTemp);
            }
        }
    }

    //Adds nMultAdd string into an array
    int arrMult[16];
    char t[17];
    sprintf(t, "%s", nMultAdd);
    lengMA = strlen(nMultAdd);
    int k;
    for (k = 0; k < leng; k++)
    {
        arrMult[k] = t[k] - '0';
    }

    //Loops through arrMult[]
    int nMultAddSum = 0;
    int j;
    for (j = 0; j < lengMA; j++)
    {
        //Sums up digits of arrMult[]
        nMultAddSum = nMultAddSum + arrMult[j];
    }

    //Sums up nMultAddSum and nAdd
    int finalSum = nMultAddSum + nAdd;

    //Gets last digit of finalSum
    int lastDigitSum = finalSum % 10;

    //Checks whether lastDigitSum is a 0
    if (lastDigitSum == 0)
    {
        //Checks whether the CCN has 16 digits
        if (leng == 16)
        {
            //Checks whether the CCN starts with 5
            if (arr[0] == 5)
            {
                if (arr[1] == 1 || arr[1] == 2 || arr[1] == 3 || arr[1] == 4 || arr[1] == 5)
                {
                    //Prints MASTERCARD
                    printf("MASTERCARD\n");
                }
                else
                {
                    //Prints INVALID
                    printf("INVALID\n");
                }
            }
            //Checks whether the CCN starts with 4
            else if (arr[0] == 4)
            {
                //Prints VISA
                printf("VISA\n");
            }
            else
            {
                //Prints INVALID
                printf("INVALID\n");
            }
        }
        //Checks whether the CCN has 15 digits
        else if (leng == 15)
        {
            //Checks whether the CCN starts with 34
            if (arr[0] == 3 && arr[1] == 4)
            {
                //Prints AMEX
                printf("AMEX\n");
            }
            //Checks whether the CCN starts with 37
            else if (arr[0] == 3 && arr[1] == 7)
            {
                //Prints AMEX
                printf("AMEX\n");
            }
            else
            {
                //Prints INVALID
                printf("INVALID\n");
            }
        }
        //Checks whether the CCN has 13 digits
        else if (leng == 13)
        {
            if (arr[0] == 4)
            {
                //Prints VISA
                printf("VISA\n");
            }
            else
            {
                //Prints INVALID
                printf("INVALID\n");
            }
        }
        else
        {
            //Prints INVALID
            printf("INVALID\n");
        }
    }
    else
    {
        //Prints INVALID
        printf("INVALID\n");
    }
}