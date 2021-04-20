from .txtJson import TxtJson
import time
import subprocess
import os

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

    
    # this method reads data from the settings file and returns it in dictionary format
    def getDict(self):

        try:
            dictReturned = TxtJson.getDict(self.path)
            return dictReturned

        # if the settings file is not present
        except FileNotFoundError:
            
            # then first we will write the settings file with default data
            self.regenerateSettingsFile()

            # waiting for the os to actaully index the file
            time.sleep(0.5)

            # then we will return dict
            dictReturned = TxtJson.getDict(self.path)
            return dictReturned



    # this method generate the file with default values
    def regenerateSettingsFile(self):


        # default settings file data
        settingsFile = """
# username - comes instead of default username in greeting line - welcome { username }
username : None


# deafult city name for weather data
cityName : None


# path for password database
pathForPassDB : None 

# Want to participate in the user experience program (True / False)
acceptUserExperienceProgram : False
        """

        # writing the file
        with open(self.path , "w+") as file:
            file.write(settingsFile)

        
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
