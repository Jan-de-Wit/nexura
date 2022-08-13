#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int compute_score(string sInput);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    //Checks scores and outputs the according string
    if (score1 > score2)
    {
        printf("Player 1 Wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 Wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}


int compute_score(string sInput)
{
    int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
    char letters[] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'};
    int i;
    int j;
    int score = 0;

    //Counts length of the string
    int sLeng = strlen(sInput);

    //Loops sLeng times
    for (i = 0; i < sLeng; i++)
    {
        //Loops 26 times
        for (j = 0; j <= 26; j++)
        {
            //Checks if lowercase sInput is the same as letters at any index
            if (tolower(sInput[i]) == letters[j])
            {
                score += POINTS[j];
                break;
            }
        }
    }
    return score;
}