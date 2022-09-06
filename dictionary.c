// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "dictionary.h"

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N][N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    return toupper(word[0]) - 'A';
}

// Sets new address for the newly added node in the list to the most recently added node
void setAddress(node *parent, node *newNode)
{
    if (parent->next == NULL)
    {
        parent->next = newNode;
        return;
    }

    setAddress(parent->next, newNode);
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *DICTIONARY = fopen(dictionary, "r");

    if (dictionary == NULL)
    {
        printf("Could not open %s.\n", dictionary);
        return false;
    }

    char word[LENGTH + 1];
    
    while (fscanf(DICTIONARY, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));
        strcpy(n->word, word);
        n->next = NULL;

        int firstLetters[2];
        firstLetters[0] = tolower(word[0]) - 97;
        firstLetters[1] = tolower(word[1]) - 97;

        setAddress(table[firstLetters[0]][firstLetters[1]], n);
    }
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    return false;
}
