#include <stdio.h>
#include <stdint.h>
#include <cs50.h>

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

int main(void)
{
    const char *str = get_string("word: ");
    const int N = 15000;
    for (int i = 0; i < N; i++)
    {
        uint32_t hashIndex = hash(str);
        hashIndex /= 0x45ed0;

        if (hashIndex < 0)
        {
            hashIndex = 0;
        }
        else if (hashIndex > N)
        {
            hashIndex = (uint32_t) N;
        }

        if (i == 0)
        {
            printf("hashIndex 1 = %i\n", hashIndex);
        }
    }
}