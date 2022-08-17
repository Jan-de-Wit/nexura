// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    // TODO: Copy header from input file to output file
    //fread to read 44 bytes and fwrite to write those 44 bytes to output.wav
    uint8_t header[44];
    fread(&header, HEADER_SIZE, 1, input);
    fwrite(&header, HEADER_SIZE, 1, output);

    // TODO: Read samples from input file and write updated data to output file
    int freadError = 0;
    int n = 0;
    int16_t sample = 0;

    do
    {
        if (fread(&sample, sizeof(int16_t), 1, input) < 1)
        {
            freadError = 1;
        }
        else
        {
            sample = sample * factor;
            fwrite(&sample, sizeof(int16_t), 1, output);
            n++;
        }
    }
    while (freadError == 0);

    if (n == 352.800 / 2)
    {
        printf("$$$ looped %i times\n", n);
    }
    else
    {
        printf("###looped %i times\n", n);
    }

    // Close files
    fclose(input);
    fclose(output);
}
