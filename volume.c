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
    uint8_t *header = malloc(HEADER_SIZE);
    fread(header, HEADER_SIZE, 1, input);
    fwrite(&input, HEADER_SIZE, 1, output);
    free(header);

    printf("Header got copied\n");

    // TODO: Read samples from input file and write updated data to output file
    int freadError = 0;
    int n = 0;
    while (freadError == 0)
    {
        printf("While loop initiated\n");
        int16_t sample = 0;
        int16_t *p = &sample;

        printf("Variables initialized\n");
        if (fread(p, sizeof(int16_t), 1, input) == 1)
        {
            printf("If statement worked");
            sample = sample * factor;
            fwrite(p, sizeof(int16_t), 1, output);
            n++;
            printf("Succesfull write %i times\n", n);
        }
        else
        {
            freadError = 1;
        }
    }
    // length of samples

    // for each sample (int16_t):
        //Read sample from input.wav
        //multiply sample by factor
        //write the new sample to output.wav

    // Close files
    fclose(input);
    fclose(output);
}
