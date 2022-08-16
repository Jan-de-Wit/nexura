#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
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
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i]) == 0)
        {
            //Ranks[rank <- indicates which rating rank]
            //= i <- indicates which index of candidates
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]]++;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    //Creates winScore (win margin)
    int pCount = 0;
    int winScore[MAX * (MAX - 1) / 2];
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (preferences[i][j] > preferences[j][i])
            {
                winScore[pCount] = preferences[i][j] - preferences[j][i];
                pCount++;
            }
        }
    }

    //Sorts pairs[] based on their winScore
    for (int i = 0; i < pair_count - 1; i++)
    {
        for (int j = 0; j < pair_count -2; j++)
        {
            if (winScore[i] < winScore[i + 1])
            {
                pair temp = pairs[i];
                pairs[i] = pairs[i + 1];
                pairs[i + 1] = temp;
            }
        }
    }
    return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    //Loops i times
    printf("pair_count is: %i\n", pair_count);
    for (int i = 0; i < pair_count; i++)
    {
        //Sets locked[i][j] to true
        locked[pairs[i].winner][pairs[i].loser] = true;
        printf("There is now a connection between winner (%i) and loser (%i)\n", pairs[i].winner, pairs[i].loser);

        int lockedCount = 0;
        // //Checks if locked[i][j] doesn't make a cycle
        // for (int j = 0; j < candidate_count; j++)
        // {
        //     //BUG : check for clockwise cycle doesnt work
        //     if (j == 0)
        //     {
        //         if (locked[j][candidate_count - 1] == true)
        //         {
        //             lockedCount++;
        //             printf("lockedCount is now %i\n", lockedCount);
        //         }
        //     }
        //     else
        //     {
        //         if (locked[j][j - 1] == true)
        //         {
        //             lockedCount++;
        //             printf("lockedCount is now %i\n", lockedCount);
        //         }
        //     }
        // }
        // if (lockedCount >= candidate_count)
        // {
        //     locked[pairs[i].winner][pairs[i].loser] = false;
        //     printf("Connection between winner (%i) and loser (%i) got removed\n", pairs[i].winner, pairs[i].loser);
        // }
        // else
        // {
            //Against the clock cycle check
            lockedCount = 0;
            for (int j = 0; j < candidate_count; j++)
            {
                if (j == candidate_count - 1)
                {
                    if (locked[j][0] == true)
                    {
                        lockedCount++;
                        printf("lockedCount is now %i\n", lockedCount);
                    }
                }
                else
                {
                    if (locked[j][j + 1] == true)
                    {
                        lockedCount++;
                        printf("lockedCount is now %i\n", lockedCount);
                    }
                }
            }
            if (lockedCount >= candidate_count)
            {
                locked[pairs[i].winner][pairs[i].loser] = false;
                printf("Connection between winner (%i) and loser (%i) got removed\n\n", pairs[i].winner, pairs[i].loser);
            }
        }
    }


// Print the winner of the election
void print_winner(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (i == 0)
        {
            if (locked[candidate_count - 1][i] == false && locked[i + 1][i] == false)
            {
                printf("%s\n", candidates[i]);
                return;
            }
        }
        else if (i == candidate_count - 1)
        {
            if (locked[0][i] == false && locked[i - 1][i] == false)
            {
                printf("%s\n", candidates[i]);
                return;
            }
        }
        else
        {
            if (locked[i - 1][i] == false && locked[i + 1][i] == false)
            {
                printf("%s\n", candidates[i]);
                return;
            }
        }
    }
    printf("printing failed lol\n");
}