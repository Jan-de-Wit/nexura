#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //Gets user input
    string answer = get_string("What is your name? ");

    //Prints "Hello <answer>"
    printf("Hello %s!\n", answer);
}