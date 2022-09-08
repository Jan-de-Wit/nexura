// Declares a dictionary's functionality

#ifndef DICTIONARY_H
#define DICTIONARY_H

#include <stdbool.h>
#include <stdint.h>

// Maximum length for a word
// (e.g., pneumonoultramicroscopicsilicovolcanoconiosis)
#define LENGTH 45

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Prototypes
bool inBucket(node *parent, const char *word, int counter);
bool check(char *word);
uint32_t hash(const char *str);
bool load(const char *dictionary);
int countBucket(node *address);
unsigned int size(void);
bool unload(void);

#endif // DICTIONARY_H
