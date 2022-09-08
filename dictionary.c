// Implements a dictionary's functionality
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>


#include "dictionary.h"

// Choose number of buckets in hash table
const unsigned int N = 15000;

// Hash table
node *table[N];

//Returns true if word is found in the linked list
bool inBucket(node *parent, const char *word, int counter)
{
    counter++;
    if (strcasecmp(parent->word, word) == 0)
    {
        return true;
    }
    else
    {
        if (parent->next != NULL)
        {
            if (!inBucket(parent->next, word, counter))
            {
                return false;
            }
            else
            {
                return true;
            }
        }
        else
        {
            return false;
        }
    }
}

// Returns true if word is in dictionary, else false
bool check(char *word)
{
    int wordLength = strlen(word);

    for (int i = 0; i < wordLength; i++)
    {
        char c = tolower(word[i]);
        word[i] = c;
    }

    uint32_t hashIndex = hash(word);
    hashIndex /= 0x45ed0;

    if (hashIndex < 0)
    {
        hashIndex = 0;
    }
    else if (hashIndex > N)
    {
        hashIndex = (uint32_t) N;
    }

    if (table[hashIndex] != NULL)
    {
        if (!inBucket(table[hashIndex], word, 0))
        {
            return false;
        }
        else
        {
            return true;
        }
    }
    else
    {
        return false;
    }
}

// Hashes word to a number
uint32_t hash(const char *str)
{
    // Source: https://stackoverflow.com/a/21001712
    unsigned int byte, crc, mask;
    int i = 0, j;
    crc = 0xFFFFFFFF;
    while (str[i] != 0) {
        byte = str[i];
        crc = crc ^ byte;
        for (j = 7; j >= 0; j--) {
            mask = -(crc & 1);
            crc = (crc >> 1) ^ (0xEDB88320 & mask);
        }
        i++;
    }
    return ~crc;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    //Opens the dictionary file
    FILE *DICTIONARY = fopen(dictionary, "r");

    //Checks whether something went wrong whilst opening the dictionary file
    if (DICTIONARY == NULL)
    {
        printf("Could not open %s.\n", dictionary);
        return false;
    }

    //Reads the dictionary in words and adds them to the buffer
    char word[LENGTH + 1];
    while (fscanf(DICTIONARY, "%s", word) != EOF)
    {
        //Creates a new node for the word read and sets the pointer to NULL
        node *n = malloc(sizeof(node));
        strcpy(n->word, word);
        n->next = NULL;

        //Calculates which bucket the letter should go into
        uint32_t hashIndex = hash(word);
        hashIndex /= 0x45ed0;

        if (hashIndex < 0)
        {
            hashIndex = 0;
        }
        else if (hashIndex > N)
        {
            hashIndex = (uint32_t) N;
        }

        if (table[hashIndex] == NULL)
        {
            table[hashIndex] = n;
        }
        else
        {
            //Inserts the new node as first in the list
            n->next = table[hashIndex];
            table[hashIndex] = n;
        }
    }
    fclose(DICTIONARY);
    return true;
}

int countBucket(node *address)
{
    int counter = 0;

    //Checks if its the last node in the list and adds a word to the counter
    if (address->next == NULL)
    {
        counter++;
        return counter;
    }
    else
    {
        //Adds a word to the counter and recalls itselves
        counter++;
        counter+= countBucket(address->next);
    }

    return counter;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    int counter = 0;

    //Sets up a for loops to iterate through all of the buckets
    for (int i = 0; i < N; i++)
    {
        //Checks if table[i][j] has a valid pointer address
        if (table[i] != NULL)
        {
            //Calls countBucket function and adds the returned value to the counter variable
            counter += countBucket(table[i]);
        }
    }

    return counter;
}

void unloadBucket(node *address)
{
    //Base case
    if (address->next == NULL)
    {
        free(address);
        return;
    }
    else
    {
        //Frees the child recursively
        unloadBucket(address->next);

        //Free parent
        free(address);
        return;
    }
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    //Sets up a for loops to iterate through all of the buckets
    for (int i = 0; i < N; i++)
    {
        //Checks if table[i][j] has a valid pointer address
        if (table[i] != NULL)
        {
            //Calls unloadBucket function to unload the bucket
            unloadBucket(table[i]);
        }
    }
    return true;
}
