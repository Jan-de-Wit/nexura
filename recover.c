#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <cs50.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    //Checks if theres more/less than 2 commandline arguments
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }
    else
    {
        int BLOCKSIZE = 512;
        FILE *raw = fopen(argv[1], "r");
        int fileCount = 0;
        BYTE buffer[512];
        FILE *img;
        bool newImage = NULL;

        while (fread(buffer, 1, BLOCKSIZE, raw) == BLOCKSIZE)
        {
            //Checks if it identifies the start of a new image
            if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && buffer[3] >= 0xe0 && buffer[3] <= 0xef)
            {
                //Checks if there was already an jpeg opened
                if (newImage == true)
                {
                    fclose(img);
                    fileCount++;
                }
                newImage = true;

                //Counts amount of digits in fileCount
                int temp = fileCount;
                int lenFC = 0;

                while (temp != 0)
                {
                    temp /= 10;
                    lenFC++;
                }

                //Creates the new file name
                char filename[lenFC + 1];
                sprintf(filename, "%.3d.jpg", fileCount);

                //Opens and writes to the new file
                img = fopen(filename, "w");
                fwrite(buffer, 1, BLOCKSIZE, img);
            }
            else if (newImage == true)
            {
                //Writes to the file
                fwrite(buffer, 1, BLOCKSIZE, img);
            }
        }
        //Closes image and ends the program
        fclose(img);
        fclose(raw);
        return 0;
    }
}