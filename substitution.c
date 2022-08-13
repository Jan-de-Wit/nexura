#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    int i;
    int j = 0;
    int lengKey;
    char keyArr[26];
    char s[27];
    char cAll[27];
    char character;
    char cTemp;
    int lengInput;
    string sAll = "";

    //Checks if there are more/less than 2 command line arguments
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    else
    {
        //Sets variable key and gets length of key
        string key = argv[1];
        lengKey = strlen(key);

        //Checks if the key is 26 characters
        if (lengKey != 26)
        {
            printf("Key must contain 26 characters.\n");
            return 1;
        }
        else
        {
            //Prompt for user input
            string sText = get_string("plaintext: ");

            //Gets length of the by user inputted string
            lengInput = strlen(sText);

            while (sText[j] != '\0')
            {
                //Sets char variable to the current value of the array
                character = sText[j];

                if (islower(sText[j]))
                {
                    //Remaps key to uppercase
                    sprintf(s, "%s", key);
                    for (i = 0; i < 27; i++)
                    {
                        keyArr[i] = tolower(s[i]);
                    }

                    switch (character)
                    {
                        //Remaps to the right value according to the key
                        case 97:
                            cTemp = keyArr[0];
                            break;
                        //Remaps to the right value according to the key
                        case 98:
                            cTemp = keyArr[1];
                            break;
                        //Remaps to the right value according to the key
                        case 99:
                            cTemp = keyArr[2];
                            break;
                        //Remaps to the right value according to the key
                        case 100:
                            cTemp = keyArr[3];
                            break;
                        //Remaps to the right value according to the key
                        case 101:
                            cTemp = keyArr[4];
                            break;
                        //Remaps to the right value according to the key
                        case 102:
                            cTemp = keyArr[5];
                            break;
                        //Remaps to the right value according to the key
                        case 103:
                            cTemp = keyArr[6];
                            break;
                        //Remaps to the right value according to the key
                        case 104:
                            cTemp = keyArr[7];
                            break;
                        //Remaps to the right value according to the key
                        case 105:
                            cTemp = keyArr[8];
                            break;
                        //Remaps to the right value according to the key
                        case 106:
                            cTemp = keyArr[9];
                            break;
                        //Remaps to the right value according to the key
                        case 107:
                            cTemp = keyArr[10];
                            break;
                        //Remaps to the right value according to the key
                        case 108:
                            cTemp = keyArr[11];
                            break;
                        //Remaps to the right value according to the key
                        case 109:
                            cTemp = keyArr[12];
                            break;
                        //Remaps to the right value according to the key
                        case 110:
                            cTemp = keyArr[13];
                            break;
                        //Remaps to the right value according to the key
                        case 111:
                            cTemp = keyArr[14];
                            break;
                        //Remaps to the right value according to the key
                        case 112:
                            cTemp = keyArr[15];
                            break;
                        //Remaps to the right value according to the key
                        case 113:
                            cTemp = keyArr[16];
                            break;
                        //Remaps to the right value according to the key
                        case 114:
                            cTemp = keyArr[17];
                            break;
                        //Remaps to the right value according to the key
                        case 115:
                            cTemp = keyArr[18];
                            break;
                        //Remaps to the right value according to the key
                        case 116:
                            cTemp = keyArr[19];
                            break;
                        //Remaps to the right value according to the key
                        case 117:
                            cTemp = keyArr[20];
                            break;
                        //Remaps to the right value according to the key
                        case 118:
                            cTemp = keyArr[21];
                            break;
                        //Remaps to the right value according to the key
                        case 119:
                            cTemp = keyArr[22];
                            break;
                        //Remaps to the right value according to the key
                        case 120:
                            cTemp = keyArr[23];
                            break;
                        //Remaps to the right value according to the key
                        case 121:
                            cTemp = keyArr[24];
                            break;
                        //Remaps to the right value according to the key
                        case 122:
                            cTemp = keyArr[25];
                            break;
                        default:
                            cTemp = character;
                            break;
                    }
                }
                else
                {
                    //Remaps key to uppercase
                    sprintf(s, "%s", key);
                    for (i = 0; i < 27; i++)
                    {
                        keyArr[i] = (int) toupper(s[i]);
                    }

                    switch (character)
                    {
                        //Remaps to the right value according to the key
                        case 65:
                            cTemp = keyArr[0];
                            break;
                        //Remaps to the right value according to the key
                        case 66:
                            cTemp = keyArr[1];
                            break;
                        //Remaps to the right value according to the key
                        case 67:
                            cTemp = keyArr[2];
                            break;
                        //Remaps to the right value according to the key
                        case 68:
                            cTemp = keyArr[3];
                            break;
                        //Remaps to the right value according to the key
                        case 69:
                            cTemp = keyArr[4];
                            break;
                        //Remaps to the right value according to the key
                        case 70:
                            cTemp = keyArr[5];
                            break;
                        //Remaps to the right value according to the key
                        case 71:
                            cTemp = keyArr[6];
                            break;
                        //Remaps to the right value according to the key
                        case 72:
                            cTemp = keyArr[7];
                            break;
                        //Remaps to the right value according to the key
                        case 73:
                            cTemp = keyArr[8];
                            break;
                        //Remaps to the right value according to the key
                        case 74:
                            cTemp = keyArr[9];
                            break;
                        //Remaps to the right value according to the key
                        case 75:
                            cTemp = keyArr[10];
                            break;
                        //Remaps to the right value according to the key
                        case 76:
                            cTemp = keyArr[11];
                            break;
                        //Remaps to the right value according to the key
                        case 77:
                            cTemp = keyArr[12];
                            break;
                        //Remaps to the right value according to the key
                        case 78:
                            cTemp = keyArr[13];
                            break;
                        //Remaps to the right value according to the key
                        case 79:
                            cTemp = keyArr[14];
                            break;
                        //Remaps to the right value according to the key
                        case 80:
                            cTemp = keyArr[15];
                            break;
                        //Remaps to the right value according to the key
                        case 81:
                            cTemp = keyArr[16];
                            break;
                        //Remaps to the right value according to the key
                        case 82:
                            cTemp = keyArr[17];
                            break;
                        //Remaps to the right value according to the key
                        case 83:
                            cTemp = keyArr[18];
                            break;
                        //Remaps to the right value according to the key
                        case 84:
                            cTemp = keyArr[19];
                            break;
                        //Remaps to the right value according to the key
                        case 85:
                            cTemp = keyArr[20];
                            break;
                        //Remaps to the right value according to the key
                        case 86:
                            cTemp = keyArr[21];
                            break;
                        //Remaps to the right value according to the key
                        case 87:
                            cTemp = keyArr[22];
                            break;
                        //Remaps to the right value according to the key
                        case 88:
                            cTemp = keyArr[23];
                            break;
                        //Remaps to the right value according to the key
                        case 89:
                            cTemp = keyArr[24];
                            break;
                        //Remaps to the right value according to the key
                        case 90:
                            cTemp = keyArr[25];
                            break;
                        default:
                            cTemp = character;
                            break;
                    }
                }
                //Remaps cTemp to an array
                cAll[j] = cTemp;
                j++;
            }
        }
    }

    //Output
    printf("ciphertext: ");

    int k;
    for (k = 0; k < lengInput; k++)
    {
        printf("%c", cAll[k]);
    }
    printf("\n");
}