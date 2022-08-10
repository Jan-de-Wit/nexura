#include <cs50.h>
#include <stdio.h>


int main(void)
{
    //Request for user input until input >1 && <8
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1 || n > 8);

    ////Drawing module

    //Cycles through the code n times
    int i;
    for (i = 0; i < n; i++)
    {
        // Prints i * "#"
        int j;
        for (j = n - i; j > 1; j--)
        {
            printf(" ");
        }

        // Prints k * "#"
        int k;
        for (k = 0; k <= i; k++)
        {
            printf("#");
        }

        // Prints "  " between two piramids
        int l;
        for (l = n; l <= n; l++)
        {
            printf("  ");
        }

        // Prints i * "#" (for the right piramid)
        int m;
        for (m = 0; m <= i; m++) {
            printf("#");
        }
        
        //Prints new line
        printf("\n");
    }
}