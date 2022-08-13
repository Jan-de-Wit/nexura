#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // TODO: Print the winner
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

int compute_score(string word)
{
    int i = 0;
    int score = 0;
    while (word[i] != '\0')
    {
        //Sets a temporary char variable
        char character = word[i];

        //Converts character to lowercase
        char cLower = tolower(character);

        if (isalpha(character))
        {
            switch (cLower)
            {
                case 97:
                    score += POINTS[0];
                    break;
                case 98:
                    score += POINTS[1];
                    break;
                case 99:
                    score += POINTS[2];
                    break;
                case 100:
                    score += POINTS[3];
                    break;
                case 101:
                    score += POINTS[4];
                    break;
                case 102:
                    score += POINTS[5];
                    break;
                case 103:
                    score += POINTS[6];
                    break;
                case 104:
                    score += POINTS[7];
                    break;
                case 105:
                    score += POINTS[8];
                    break;
                case 106:
                    score += POINTS[9];
                    break;
                case 107:
                    score += POINTS[10];
                    break;
                case 108:
                    score += POINTS[11];
                    break;
                case 109:
                    score += POINTS[12];
                    break;
                case 110:
                    score += POINTS[13];
                    break;
                case 111:
                    score += POINTS[14];
                    break;
                case 112:
                    score += POINTS[15];
                    break;
                case 113:
                    score += POINTS[16];
                    break;
                case 114:
                    score += POINTS[17];
                    break;
                case 115:
                    score += POINTS[18];
                    break;
                case 116:
                    score += POINTS[19];
                    break;
                case 117:
                    score += POINTS[20];
                    break;
                case 118:
                    score += POINTS[21];
                    break;
                case 119:
                    score += POINTS[22];
                    break;
                case 120:
                    score += POINTS[23];
                    break;
                case 121:
                    score += POINTS[24];
                    break;
                case 122:
                    score += POINTS[25];
                    break;
            }
        }
        i++;
    }
    return score;
}
