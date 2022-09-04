#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }
    else
    {
        return 0;

        int BLOCKSIZE = 512;
        FILE *raw = fopen(argv[1], "r");
        int fileCount = -1;
        BYTE *buffer = malloc(512);

        while (fread(buffer, 1, BLOCKSIZE, raw) == BLOCKSIZE)
        {
            int newImage = 2;

            if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff)
            {
                if (buffer[3] >= 0xe0 && buffer[3] <= 0xef)
                {
                    newImage = 1;
                }
            }

            if (newImage == 1)
            {
                //Open new file and start writing in there
                fileCount++;

                int temp = fileCount;

                int lenFC = 0;
                while (temp != 0)
                {
                    temp /= 10;
                    lenFC++;
                }

                char filename[lenFC + 1];


                sprintf(filename, "%.3d.jpg", fileCount);

                FILE *newJpg = fopen(filename, "w");

                fwrite(buffer, 1, BLOCKSIZE, newJpg);

                fclose(newJpg);
            }
            else if (newImage == 0)
            {
                //Continue writing in the same file
                int lenFC = 0;
                while (fileCount != 0)
                {
                    fileCount /= 10;
                    lenFC++;
                }

                char filename[lenFC + 1];

                sprintf(filename, "%.3d.jpg", fileCount);

                FILE *jpg = fopen(filename, "w");

                fwrite(buffer, 1, BLOCKSIZE, jpg);

                fclose(jpg);
            }
        }
        free(buffer);
        return 0;
    }
}