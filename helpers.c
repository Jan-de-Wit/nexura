#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int average = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);

            image[i][j].rgbtRed = average;
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp;
    int n = width / 2;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < n; j++)
        {
            temp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = temp;
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //Copies image into orgImage array to keep the original colors
    RGBTRIPLE orgImage[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            orgImage[i][j] = image[i][j];
        }
    }

    //Iterates through every row
    for (int i = 0; i <= height; i++)
    {
        //Iterates through every column
        for (int j = 0; j <= width; j++)
        {
            float counter = 0;
            int allRed = 0;
            int allGreen = 0;
            int allBlue = 0;

            int row[] = {i - 1, i, i + 1, i - 1, i, i + 1, i - 1, i, i + 1};
            int column[] = {j - 1, j, j + 1, j - 1, j, j + 1, j - 1, j, j + 1};

            for (int y = 0; y < 3; y++)
            {
                for (int x = 0; x < 3; x++)
                {
                    if (row[y] >= 0 && row[y] <= height - 1)
                    {
                        if (column[x] >= 0 && column[x] <= width - 1)
                        {
                            allRed += orgImage[row[y]][column[x]].rgbtRed;
                            allGreen += orgImage[row[y]][column[x]].rgbtGreen;
                            allBlue += orgImage[row[y]][column[x]].rgbtBlue;
                            counter++;
                        }
                    }
                }
            }

            int red = round(allRed / counter);
            int green = round(allGreen / counter);
            int blue = round(allBlue / counter);

            image[i][j].rgbtRed = red;
            image[i][j].rgbtGreen = green;
            image[i][j].rgbtBlue = blue;
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE orgImage[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            orgImage[i][j] = image[i][j];
        }
    }

    //Gx and Gy values in order from left to right from top to bottom
    int GxValue[] = {-1, 0, 1, -2, 0, 2, -1, 0, 1};
    int GyValue[] = {-1, -2, -1, 0, 0, 0, 1, 2, 1};

    //Iterates through every row
    for (int i = 0; i <= height; i++)
    {
        //Iterates through every column
        for (int j = 0; j <= width; j++)
        {
            int counter = 0;

            float GxRed = 0;
            float GxGreen = 0;
            float GxBlue = 0;

            float GyRed = 0;
            float GyGreen = 0;
            float GyBlue = 0;

            int row[] = {i - 1, i, i + 1, i - 1, i, i + 1, i - 1, i, i + 1};
            int column[] = {j - 1, j, j + 1, j - 1, j, j + 1, j - 1, j, j + 1};

            for (int y = 0; y < 3; y++)
            {
                for (int x = 0; x < 3; x++)
                {
                    if (row[y] >= 0 && row[y] <= height - 1)
                    {
                        if (column[x] >= 0 && column[x] <= width - 1)
                        {
                            GxRed += (orgImage[row[y]][column[x]].rgbtRed * GxValue[counter]);
                            GxGreen += (orgImage[row[y]][column[x]].rgbtGreen * GxValue[counter]);
                            GxBlue += (orgImage[row[y]][column[x]].rgbtBlue * GxValue[counter]);

                            GyRed += (orgImage[row[y]][column[x]].rgbtRed * GyValue[counter]);
                            GyGreen += (orgImage[row[y]][column[x]].rgbtGreen * GyValue[counter]);
                            GyBlue += (orgImage[row[y]][column[x]].rgbtBlue * GyValue[counter]);
                            printf("GxR: %f, GyR: %f counter: %i", GxRed, GyRed, counter);

                            counter++;
                        }
                        else
                        {
                            counter++;
                        }
                    }
                    else
                    {
                        counter+= 3;
                    }
                }
            }

            int gRed = (GxRed * GxRed) + (GyRed * GyRed);
            int gGreen = (GxGreen * GxGreen) + (GyGreen * GyGreen);
            int gBlue = (GxBlue * GxBlue) + (GyBlue * GyBlue);

            if (gRed > 255)
            {
                gRed = 255;
            }
            else if (gRed < 0)
            {
                gRed = 0;
            }
            if (gGreen > 255)
            {
                gGreen = 255;
            }
            else if (gGreen < 0)
            {
                gGreen = 0;
            }
            if (gBlue > 255)
            {
                gBlue = 255;
            }
            else if (gBlue < 0)
            {
                gBlue = 0;
            }

            image[i][j].rgbtRed = gRed;
            image[i][j].rgbtGreen = gGreen;
            image[i][j].rgbtBlue = gBlue;

            printf("$$$R: %i, G: %i & B: %i\n", gRed, gGreen, gBlue);
        }
    }
    return;
}
