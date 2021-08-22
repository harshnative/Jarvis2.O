# from .txtJson import TxtJson
import time
import subprocess
import os
import hjson
import copy

# main class
class SettingsClass:

    # constructor for the class
    def __init__(self , windowsPathSimple , linuxPath , isOnWindows ,isOnLinux):
        
        # making pass variable to self variables so that they can accessed by all function in the class
        self.windowsPath = windowsPathSimple + "/settings.txt"
        self.linuxPath = linuxPath + "/settings.txt"
        self.isOnWindows = isOnWindows
        self.isOnLinux = isOnLinux


        # setting up the settings file path based the operation system of the user
        self.path = None
        
        if(self.isOnWindows):
            self.path = self.windowsPath
        elif(self.isOnLinux):
            self.path = self.linuxPath

        # default settings file data
        self.settingsFile = {
  "userName": "None" , 
  "cityName": "None" , 
  "path_for_password_db": "None" , 
  "accept_user_experience_program": "None" , 
  "userName_fileShare": "None" , 
  "password_fileShare": "None" , 
  "defaultFolderFileShare": "None", 
  "defaultUserName": "None",
  "fileShareIn_V_Mode": "None" , 
  "autoAddFileToUser": "None" , 
  "timeDelayInAutoAddFile": "10" , 
}

    
    # this method reads data from the settings file and returns it in dictionary format
    def getDict(self):

        try:

            with open(self.path , "r") as file:
                data = file.read()

            dictReturned = hjson.loads(data)

            if(len(dictReturned) < len(self.settingsFile)):
                tempSettings = copy.deepcopy(self.settingsFile)

                tempSettings.update(dictReturned)

                self.regenerateSettingsFile(tempSettings)

                return tempSettings

            else:
                return dictReturned

        # if the settings file is not present
        except FileNotFoundError:
            
            # then first we will write the settings file with default data
            self.regenerateSettingsFile()

            # waiting for the os to actaully index the file
            time.sleep(0.5)

            # then we will return dict
            with open(self.path , "r") as file:
                data = file.read()

            dictReturned = hjson.loads(data)
            return dictReturned

    # this method generate the file with default values
    def regenerateSettingsFile(self , settingsFile = None):

        if(settingsFile == None):
            settingsFile = self.settingsFile

        # writing the file
        with open(self.path , "w+") as file:
            file.write(hjson.dumps(settingsFile))



        
    # function to open the settings using default opener
    # None is retruned on succesfull opening 
    # exception in string format is returned else wise
    def openSettings(self):
        try:
            # startfile utility on windows
            if(self.isOnWindows):
                os.startfile(self.path)
            else:
                # using gedit on linux
                os.system("sudo gedit " + self.path)
            return None
        except Exception as e:
            return str(e)
