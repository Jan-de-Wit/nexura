#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Function prototypes
bool vote(string name, int c);
void print_winner(int c);

int main(int argc, string argv[])
{
    // Number of candidates
    int candidate_count;

    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name, candidate_count))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner(candidate_count);
}

// Update vote totals given a new vote
bool vote(string name, int c)
{
    int leng = strlen(name);
    for (int i = 0; i < leng; i++)
    {
        if (isalpha(name[i]) == 0)
        {
            return false;
        }
    }

    for (int i = 0; i < c; i++)
    {
        if (strcmp(name, candidates[i].name) == 0)
        {
            candidates[i].votes++;
            return true;
        }
    }
    return false;
}

// Print the winner (or winners) of the election
void print_winner(int c)
{
    for (int i = 0; i < c - 1; i++)
    {
        for (int j = 0; j < c - 2; j++)
        {
            if (candidates[i].votes > candidates[i + 1].votes)
            {
                //Swaps votes
                int iTemp = candidates[i].votes;
                candidates[i].votes = candidates[i + 1].votes;
                candidates[i+1].votes = iTemp;

                //Swaps names
                string sTemp = candidates[i].name;
                candidates[i].name = candidates[i + 1].name;
                candidates[i+1].name = sTemp;
            }
        }
    }

    int iLastDigit = candidates[c - 1].votes % 10;

    for (int i = 0; i < c; i++)
    {
        if (iLastDigit == candidates[i].votes % 10)
        {
            printf("%s\n", candidates[i].name);
        }
    }
}