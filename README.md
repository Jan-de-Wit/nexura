# Rapit Standalone CLI API Program
#### Video Demo: https://www.youtube.com/watch?v=tmM3EVjG824
#### Description:

###### [This program is part of a project made by Jan de Wit, which also includes a server side integration.]  
###### [There, the user will be able to access their uploaded data using the GUI.]
###### [However, for safety purposes, the server side of the program will not be made accessible to the public.]  

This program will process and upload the needed data to the Rapit Servers.

## How to use the program
To use this program, you must run the backupHandler.py file (for the users, this will be the .exe executable file).  

Once the program has started, it prompts the user for the email address that is used in the user's account on Rapit.  
After that it'll prompt for the user's password on Rapit.  

It shall then make a request to the server to make sure that the user is a authoritized user of the application.  

Next up, it'll prompt the user for the password that is used to encrypt the iCloud backup with (which is found in iTunes). And finally it will prompt the user for the location of the backup folder, specifically the folder in which the manifest file is located. E.g. C:\Users\User\Apple\MobileSync\Backup\randomCharacters.  

## Possible Errors
### ["Error: Backup Password Invalid."]
This means that the password that was used to encrypt the backup with, was incorrect. To fix this, you can restart the program and supply the right credentials.  

### ["Error: Failed to establish a new connection: [WinError 10061] No connection could be made because the target machine actively refused it'))"]
This means that no connection could be made to the server. This can happen if the website is offline, or if there is no internet connection available. To fix this, you can check your connection, and the server status.  
- If you don't have an internet connection available, you'd have to connect to a WiFi network or hotspot.
- If the server is offline, you'll have no option but to wait until it's back online.  

### ["Error: "[SERVER]: {error is not defined}"]
This means that there was an error on the server, the message between the curly braces will tell you what happened. If you've seen one of these, please reach out to me and tell me what you've done to get it and what the error message is.  

### ["Error: Wrong account credentials]
This means that the the password is incorrect. To fix this, you'll need to find the AppData folder on your device (which is displayed in the terminal that opens up when you launch the application), and in that folder you'll need to find the config.json file. Finally you'd need to edit the config.json file so that the data that is in there, is correct. For example, if you'd like to change the password, you'd have to change it like the following:
- [BEFORE] {"email": "example@eg.com", "password": "123$OldPassword"}
- [AFTER] {"email": "example@eg.com", "password": "NewPassword#123"}  
