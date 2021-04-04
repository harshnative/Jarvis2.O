# essential modules
import os
import platform
import time
import sys
import subprocess as sp
from threading import Thread
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
from packages.logger import loggerpy 
import multiprocessing
import sys
import getpass



# declaring some global variables
class GlobalData_main:

    # current version of software
    currentVersion = 0.1

    # variables to determine the operating system of the user 
    isOnWindows = False
    isOnLinux = False

    # variables to manage the loading animation 
    runLoadingAnimation = True
    loadingAnimationCount = 5
    lAnimationObj = None


    # path for storing the program files
    folderPathWindows = r"C:\programData\JarvisData"
    folderPathLinux = ""
    folderPathWindows_simpleSlash = r"C:/programData/JarvisData"


    # obj for logger module
    objClogger = None
    troubleshootValue = False

    # dict from the settings file will be stored here
    settingDict = None


    # variable for file share module
    portForFileShare = 5000 
    isFileShareStarted = False
    addressForShare = None
    dataListFileShare = []

    # obj to store tk object
    root = None

    # list holding info about running background operations
    printDataList = []

    # toUpgradeJarvis handler
    toUpgradeJarvis = False

    # username in setting + username in PC storer
    userCP = ""

    # tempInputter
    tempInput = ""
    tempInputToShow = ""

    # driver function reference
    driverFuncReference = None




# function to reset the temp input values
def resetTempInput():
    GlobalData_main.tempInput = ""
    GlobalData_main.tempInputToShow = ""



















# Checking the users operating system and adding data to global class
osUsing = platform.system()

if(osUsing == "Linux"):
    GlobalData_main.isOnLinux = True
    if(sys.argv[0] == "jarvis.py"):
        GlobalData_main.troubleshootValue = True
        GlobalData_main.folderPathLinux = os.getcwd() + "/JarvisData"
    else:
        GlobalData_main.folderPathLinux = "/opt/JarvisData"

    # making the program data folder
    try:
        os.mkdir(GlobalData_main.folderPathLinux)
    except FileExistsError:
        pass
    except PermissionError:
        print("\nPlease run jarvis using sudo")
        sys.exit()

elif(osUsing == "Windows"):
    GlobalData_main.isOnWindows = True

    # making the program data folder
    try:
        os.mkdir(GlobalData_main.folderPathWindows)
    except FileExistsError:
        pass

else:
    print("Jarvis currently does not support this operating system :(")
    time.sleep(3)
    sys.exit()

del osUsing































# clear screen function 
def customClearScreen():
    if(GlobalData_main.isOnWindows == True):
        os.system("cls")
    else:
        sp.call('clear',shell=True)








































def resetLoggerObj():
    # setting up the logger module
    try:
        GlobalData_main.objClogger = loggerpy.Clogger(GlobalData_main.isOnWindows , GlobalData_main.isOnLinux , GlobalData_main.folderPathWindows_simpleSlash , GlobalData_main.folderPathLinux)
    except PermissionError:
        print("\nPlease run jarvis using sudo")
        sys.exit()

    GlobalData_main.objClogger.setTroubleShoot(GlobalData_main.troubleshootValue)


if __name__ == "__main__":
    resetLoggerObj()




# loading animation thread
class LoadingAnimation(Thread):

    def run(self):

        customClearScreen()
        string = ""

        # will run only till max 5 times or early if the global var runLoadingAnimation is made false
        while(GlobalData_main.runLoadingAnimation and GlobalData_main.loadingAnimationCount):
            string = string + "."
            time.sleep(0.5)
            print("\rloading , please wait " , string , end = "")
            GlobalData_main.loadingAnimationCount -= 1

        print()






# starting in the main to avoide awakeness by sub processes
if __name__ == "__main__":
    multiprocessing.freeze_support()

    # loading animation thread started 
    GlobalData_main.lAnimationObj = LoadingAnimation()
    GlobalData_main.lAnimationObj.start()




























# importing additional modules
from easyOpenWeather import module as owm
from tabulate import tabulate
import requests
import webbrowser
import datetime

from packages.speedTest import speedTestFile
from packages.settingM import settingsFile
from packages.passwordStorer import mainCode



# importting components for file share functionality
from packages.fileShare import FS
from tkinter import filedialog
from tkinter import *

if __name__ == "__main__":
    GlobalData_main.root = Tk()
    GlobalData_main.root.withdraw()






























# class containing some of the global methods
class GlobalMethods:

    # method for comparing if a string as a certain substring
    @classmethod
    def isSubString(cls , string , subString):
        lengthOfSubString = len(subString)
        try:
            """ for substring to be string - 
                1. check if the first of substring matches the string as certain i position
                2. for that i , check wheather the next characters also matches the substring till i + length of substring"""

            for i, j in enumerate(string):
                if(j == subString[0]):
                    if(subString == string[i:i+lengthOfSubString]):
                        
                        # logging the result for debugging purpose
                        GlobalData_main.objClogger.log("subString found in GlobalMethod class isSubString function , values(string , subString) = ({} , {})".format(string , subString) , "i")
                        return True
                    else:
                        pass

            # logging the result for debugging purpose
            GlobalData_main.objClogger.log("subString not found in GlobalMethod class isSubString function , values(string , subString) = ({} , {})".format(string , subString) , "i")
            return False

        except Exception as e:

            # logging the error
            GlobalData_main.objClogger.exception(str(e) , "Error in GlobalMethod class isSubString function , values(string , subString) = ({} , {})".format(string , subString))
            return False



    # method for checking if the substring is in string using list
    @classmethod
    def isSubStringsList(cls , string , subString):

        """ This method check is this way :
            normal substring check - string(hello world , this is jarvis) , subString(this jarvis) -> False
            using list substring check - string(hello world , this is jarvis) , subString(this jarvis) -> True
            compares the invidual words as substring"""

        # converting them to same case
        string = string.upper()
        subString = subString.upper()

        # getting the list of words in substring sperated by space
        subStringList = subString.split()

        # vars to keep track of number of successfull comparisions
        count1 = 0
        count2 = 0

        for i in subStringList:
            # striping the leading and trailing spaces of word in sub string list
            i = i.strip()

            # increasing the count1 as we have traversed a word
            count1 += 1

            # if this word is also a substring then we increase the count2 as well
            if(cls.isSubString(string , i)):
                count2 += 1
            else:
                # returned false as now substring is not in string
                return False

        # if the count1 matches the count2 and count1 should be greater than 0 then substring is in string
        if((count1 == count2) and count1 > 0):
            return True
        else:
            return False






































# class to get the wheather details
class WeatherFunctionality:
    
    def __init__(self):
        
        # making the object
        self.moduleObj = owm.WeatherDataClass()

        # set the api key here
        # it is removed before commiting for security reasons
        self.__apiKey = "fe82651e607e46db61dba45e39aa7e17"

        # if the custom api key is not setted then the default api key present with the module will be used
        if(self.__apiKey != ""):
            self.moduleObj.setApiKey(self.__apiKey)
    

    # driver function
    def returnDataDict(self , cityName):

        # setting the city name as per https://github.com/harshnative/easyOpenWeather_module
        self.moduleObj.setCityName(cityName)
    
        # these the things for which the data will be retreived
        listPass = ["tempInC" , "tempMin" , "tempMax" , "pressure" , "humidity" , "windSpeed" , "windDirection" , "clouds" , "description"]
        self.moduleObj.setList(listPass)


        try:
            # returning the info in dict form
            finalResult = self.moduleObj.getInfo()
            
            # logging the result for debugging purpose
            GlobalData_main.objClogger.log("weather details retrieved successfully in weather functionality class returnDataDict function , values(cityName) = ({})".format(cityName) , "i")

            return finalResult

        except Exception as e:

            # logging the error
            GlobalData_main.objClogger.exception(str(e) , "Exception in getting the weather details in WeatherFunctionality class and returnDataDict function , values(cityName) = ({})".format(cityName))
            
            return "error , could not get the weather details :("

































# class for settings functionality
class Settings:

    # setting up the object 
    settingObj = settingsFile.SettingsClass(GlobalData_main.folderPathWindows_simpleSlash , GlobalData_main.folderPathLinux , GlobalData_main.isOnWindows , GlobalData_main.isOnLinux)

    # method to return the dict
    @classmethod
    def returnDict(cls):
        try:
            returnedDict = cls.settingObj.getDict()
            GlobalData_main.objClogger.log("settings dict returned successfully in returnDict function in settings class with dict = {}".format(returnedDict) , "i")
        except Exception as e:
            GlobalData_main.objClogger.exception(str(e) , "error in settingObj.getDict() function")

        return returnedDict

    # method to open the settings file
    # returns True on successfull opening 
    # else returns false and logs error
    @classmethod
    def openSettingsFile(cls):
        result = cls.settingObj.openSettings()

        if(result == None):
            GlobalData_main.objClogger.log("settings file opened successfully" , "i")
            return True
        else:
            GlobalData_main.objClogger.exception(str(result) , "Exception in opening the settings file")
            return False

    
    # method to restore the settings file with default settings
    @classmethod
    def restoreSettings(cls):
        try:
            cls.settingObj.regenerateSettingsFile()
            GlobalData_main.objClogger.log("settings file restored succesfully successfully" , "i")
            return True
        except Exception as e:
            GlobalData_main.objClogger.exception(str(e) , "error in restoring the settings file")
            return False























class Help:
    pass
























# class to implement the file share functionality
class FileShareClass:


    # some class vars
    fil = FS.FileShareClass()
    path = None 

    
    # function to set the share path for the file share
    # open the tk gui window and then stores the returned path in class var
    # return False if process fails else return True
    @classmethod
    def setSharePath(cls):
        try:
            folder_selected = filedialog.askdirectory()
            GlobalData_main.objClogger.log("file share path setted successfully" , "i")
        except Exception as e:
            GlobalData_main.objClogger.exception(str(e) , "Exception in getting folder path from tkinter window")
            return False

        cls.path = folder_selected
        return True




    # function to start the file share 
    # returns None in case of process failure
    # else returns a list of output from module
    @classmethod
    def startFileShare(cls , http = False):
        try:
            result = cls.fil.start_fileShare(cls.path , http=http , port=GlobalData_main.portForFileShare)
            GlobalData_main.dataListFileShare = result
            GlobalData_main.addressForShare = cls.fil.get_ip_address()
            GlobalData_main.printDataList.append("File Share active at {}:{}".format(str(GlobalData_main.addressForShare) , str(GlobalData_main.portForFileShare)))
            GlobalData_main.objClogger.log("file share server started at {}".format(str(cls.path)) , "i")
            GlobalData_main.isFileShareStarted = True
            return result
        except Exception as e:
            GlobalData_main.objClogger.exception(str(e) , "Exception in starting the file share server at {}".format(str(cls.path)))
            return None

    
    # function to stop the file share module
    # return True if process completes
    # else returns False
    @classmethod
    def stopFileShare(cls):
        try:
            cls.fil.stopFileShare()
            cls.fil = FS.FileShareClass()
            GlobalData_main.printDataList.clear()
            try:
            	GlobalData_main.printDataList.remove("File Share active at {}:{}".format(str(GlobalData_main.addressForShare) , str(GlobalData_main.portForFileShare)))
            except Exception as e:
            	GlobalData_main.printDataList.clear()
            GlobalData_main.isFileShareStarted = False
            GlobalData_main.objClogger.log("file share server stopped at {}".format(str(cls.path)) , "i")
            
            return True
        except Exception as e:
            GlobalData_main.objClogger.exception(str(e) , "Exception in stopping the file share server at {}".format(str(cls.path)))
            return False
































class versionChecker(Thread):

    def run(self):
        try:

            # getting the response from website api
            response = requests.get("https://www.letscodeofficial.com/jarvis_version").json()
            
            # reponse is like [{"version": 0.1}] so getting the dict from index 0
            dictResponse = response[0]

            currentVersion = GlobalData_main.currentVersion
            versionFromResponse = dictResponse.get('version')

            # comparing the versions
            if(versionFromResponse > currentVersion):
                GlobalData_main.toUpgradeJarvis = True

            GlobalData_main.objClogger.log("jarvis new version thread runned succesfully with version from response = {} and current version = {}".format(str(versionFromResponse) , str(currentVersion)) , "i")

        except Exception as e:
                GlobalData_main.objClogger.exception(str(e) , "Exception in get version thread")

    
    

























class TroubleShooter:

    @classmethod
    def uploadFile(cls):
        # getting the log file path
        logFilePath = GlobalData_main.objClogger.returnLogFilePath()

        # opening the log file and storing it in variable
        try:
            logFile = open(logFilePath , 'rb')
            GlobalData_main.objClogger.log("Log file get procedure done successfully in TroubleShooter upload file function" , "i")
        except Exception as e:
            GlobalData_main.objClogger.exception(str(e) , "Could not get the log file")
            return 0
        
        # uploading the file to the server api using request method
        try:
            response = requests.post('https://letscodeofficial.com/upload_jarvisLog/' , files={"file": logFile} , data={"remark" : str(GlobalData_main.userCP + " upload on {}".format(str(datetime.datetime.now())))})
            GlobalData_main.objClogger.log("Log file uploaded successfully in Troubleshooter class upload file function with remark value = {}".format(str(GlobalData_main.userCP + " upload on {}".format(str(datetime.datetime.now())))) , "i")
        except ConnectionError:
            return 1
        except Exception as e:
            GlobalData_main.objClogger.exception(str(e) , "Error in uploading the log file")
            return 2

        # checking the response from the api 
        if(str(response) == "<Response [201]>"):
            return 3
        else:
            GlobalData_main.objClogger.log("response = {} in tourbleshooter class upload file function".format(response) , "e")
            return 4



    @classmethod
    def startTroubleshooter(cls):

        
        # showing the declaration
        yield "clear screen"
        yield "You are entering the troubleshooter.\n"
        yield "Program will log some info regarding errors and then upload the log file to server.Program will log some info regarding errors and then upload the log file to server.\n"
        yield "Logger does not log any sensitive information, but commands runned during troubleshooter and info of function runned by those commands will be logged.\n"
        
        # accepting the user aggrement to data share
        resetTempInput()
        GlobalData_main.tempInputToShow = "\n\nType yes to continue or anything else to quit : "
        yield "#take input#"
        continueORnot = GlobalData_main.tempInput
        resetTempInput()

        if(not(continueORnot.lower().strip() == "yes")):
            yield "\n\nTrouble shoot ended..."
            return

        # resetting the troubleshooter with INFO LEVEL logging
        GlobalData_main.troubleshootValue = True
        resetLoggerObj()

        # telling user to run the command again which caused the error
        yield "clear screen"
        yield "\n\nCan you please run the command again which caused error :)\n"

        resetTempInput()
        GlobalData_main.tempInputToShow = "Enter Command : "
        yield "#take input#"
        command = GlobalData_main.tempInput
        resetTempInput()

        yield "clear screen"

        # priting the result from driver function
        for i in GlobalData_main.driverFuncReference(command):
            yield i

        resetTempInput()
        GlobalData_main.tempInputToShow = "\n\nPress enter to upload log : "
        yield "#take input#"
        resetTempInput()

        yield "\n\nUploading log file to server please wait ..."

        result = cls.uploadFile()

        yield "clear screen"

        if(result == 0):
            yield "jarvis could not get the log file"

        elif(result == 1):
            yield "jarvis is not connected to network, you should run upload log file command when internet comes back"
        
        elif(result == 2):
            yield "jarvis could not upload the log file to server, you may mail it at letscodeoffical.com with title = 'jarvis logs' , log file is present at path = {}".format(GlobalData_main.objClogger.returnLogFilePath())
        
        elif(result == 3):
            yield "jarvis log file uploaded successfully to server , jarvis team will investigate the bug now"
        
        elif(result == 4):
            yield "jarvis could not upload the log file to server, you may mail it at letscodeoffical.com with title = 'jarvis logs' , log file is present at path = {}".format(GlobalData_main.objClogger.returnLogFilePath())


        

    @classmethod
    def uploadFileAgain(cls):
        yield "clear screen"
        yield "\n\nUploading log file to server please wait ..."

        result = cls.uploadFile()

        yield "clear screen"

        if(result == 0):
            yield "jarvis could not get the log file"

        elif(result == 1):
            yield "jarvis is not connected to network, you should run upload log file command when internet comes back"
        
        elif(result == 2):
            yield "jarvis could not upload the log file to server, you may mail it at letscodeoffical.com with title = 'jarvis logs' , log file is present at path = {}".format(GlobalData_main.objClogger.returnLogFilePath())
        
        elif(result == 3):
            yield "jarvis log file uploaded successfully to server , jarvis team will investigate the bug now"
        
        elif(result == 4):
            yield "jarvis could not upload the log file to server, you may mail it at letscodeoffical.com with title = 'jarvis logs' , log file is present at path = {}".format(GlobalData_main.objClogger.returnLogFilePath())



















# main driver function for executing commands
def driver(command):

    """No print is used before main to keep the functions modular , just return the result to main in list form or yield form"""
    
    # if the update jarvis command is passed
    if(GlobalMethods.isSubStringsList(command , "update jarvis")):
        try:
            webbrowser.open("https://www.letscodeofficial.com/jarvis_downloads")
            GlobalData_main.objClogger.log("started webbrowser to update jarvis" , "i")
            yield "jarvis download page opened in a web browser"
            return True

        except Exception as e:
            GlobalData_main.objClogger.exception(str(e) , "Exception in starting the webbrowser to update jarvis")
            yield "could not open the download page in web browser"
            yield "you can visit https://www.letscodeofficial.com/jarvis_downloads to download manually"
            return True





    # if the weather command is passed
    if(GlobalMethods.isSubStringsList(command , "weather")):

        # getting the default city name
        cityNameFromSet = GlobalData_main.settingDict.get("cityName" , "None")

        # getting the city name from command(weather cityName)
        cityName = command[len("weather") + 1:]

        cityName = cityName.strip()
        
        # if the city name is None is settings file and also city name is not passed in command then error will be returned to user
        if((cityNameFromSet == "None") and (len(cityName) <= 1)):
            yield "please pass the city name like weather london or set the default city name in settings file"
            yield "\nYou can open settings file by typing settings command"
            return True

        # else if city is not passed then it will be taken from the settings file
        elif((len(cityName) <= 1)):
            cityName = cityNameFromSet
            

        # getting the result from the class
        weatherObj = WeatherFunctionality()

        result = weatherObj.returnDataDict(cityName)

        # if the api key is not set then return the message
        if(result == None):
            yield "please set the api key"
            return True
        
        if(result == "error"):
            yield "please pass a correct city name"
            return True

        # else conv the dict returned into list with [[key] , [value]]
        resultList = []

        try:
            for i , j in result.items():
                tempList = []
                tempList.append(i)
                tempList.append(j)
                resultList.append(tempList)
        except Exception as e:
            GlobalData_main.objClogger.exception(str(e) , "Exception in getting the weather details of city = {}".format(str(cityName)))
            yield "could not get the wheather details of city : {} , sorry :(".format(cityName)
            return True

        # using the tabulate module to pretify the output
        toReturn = tabulate(resultList , headers=['Query', 'Data'])

        # returning the result so it can be printed
        yield toReturn
        return True



















    # if the speed test  command is passed
    if(GlobalMethods.isSubStringsList(command , "speed test")):
        sObj = speedTestFile.SpeedTestClass(GlobalData_main.objClogger)

        # spliting the command to get command list
        commandList = command.split()

        inBytes = False
        numberOfTimes = 2

        # if user wants result in bytes instead of bits
        if(("-b" in commandList) or ("-B" in commandList)):
            inBytes = True

        # finding the user as passed number of times
        for i in commandList:
            if(i.isnumeric()):
                if(int(i) <= 5):
                    numberOfTimes = int(i)
        


        for i in sObj.runSpeedTestUtility(inBytes=inBytes , numberOfTimesToDo=numberOfTimes):
            yield i
        
        return True





















    # if the setting command is passed
    if(GlobalMethods.isSubStringsList(command , "setting")):

        # if update setting command is passed
        if(GlobalMethods.isSubStringsList(command , "update")):
            GlobalData_main.settingDict = Settings.returnDict()
            yield "new settings applied ..."
            return True
        
        # if update setting command is passed
        if(GlobalMethods.isSubStringsList(command , "restore")):
            result = Settings.restoreSettings()
            if(result):
                yield "settings restored to default values ..."
            else:
                yield "error in restoring the settings file , try running troubleshoot command"

            return True

        # if update setting command is passed
        if(GlobalMethods.isSubStringsList(command , "open")):
            if(Settings.openSettingsFile()):
                yield "clear screen"
                yield "Settings file opened"
                yield "\nDon't forget to save it and run the update command after wards"
                return True
            else:
                yield "Error opening the settings file , Try running the troubleshoot command"
                return True























    # if the password command is passed
    if(GlobalMethods.isSubStringsList(command , "password")):

        # getting the path from settings dict
        customPath = GlobalData_main.settingDict.get("pathForPassDB")


        # if path is not setted then simply create new db
        if(customPath.lower() == "none"):
            customPath = None
        else:

            # if the path is setted but is incorrect or jarvis does not have permission to read write at that file dir then simply promt a message
            if(not(os.path.isfile(customPath))):
                print("Path specified in settings file for \"pathForPassDB\" is either incorrect or jarvis does not permission to read write their.\npassword module will create a new data base now")

                inputted = input("\n\nEnter 1 to continue or anything else to quit")
                
                if(inputted != 1):
                    yield "clear screen"
                    yield "cannot open password db"
                    return True
                    

        # waking the driver function of password module
        obj = mainCode.PasswordStorerClass(GlobalData_main.isOnWindows , GlobalData_main.isOnLinux , GlobalData_main.folderPathWindows_simpleSlash , GlobalData_main.folderPathLinux , customPath)
        obj.driverFunc()

        yield "clear screen"
        yield "exitted password db"
        return True
    




















    # if set port command is passed
    if(GlobalMethods.isSubStringsList(command , "set file port")):

        # splitting the command string to get a list
        commandList = command.split()

        port = 5000

        # traversing the command list until a numeric value is found as i
        # then set that numeric value as port
        for i in commandList:
            i = str(i)
            if(i.isnumeric()):
                port = i
            
        port = int(port)

        # port must be btw 1000 and 9999
        if((port < 1000) or (port > 9999)):
            yield "port number must be a four digit integer"
            return True
        
        # setting the port number to global var
        GlobalData_main.portForFileShare = int(port)
        yield "port number setted to {}, now you can start the file share with this port".format(str(port))
        return True






    # if stop file share command is passed
    if(GlobalMethods.isSubStringsList(command , "stop file")):

        if(GlobalData_main.isFileShareStarted):
            status = FileShareClass.stopFileShare()

            if(not(status)):
                yield "fileShare module could not stop the process"
                return True
        
            yield "filShare Stopped successfully"
            return True
        
        else:
            yield "file share is not running"
            return True



    # if the start file share command is passed
    if(GlobalMethods.isSubStringsList(command , "start file")):

        status = FileShareClass.setSharePath()

        if(not(status)):
            yield "fileShare module could not get path, Try again"
            return True

        http = False

        if(GlobalMethods.isSubStringsList(command , "http")):
            http = True

        result = FileShareClass.startFileShare(http=http)

        if(result == None):
            yield "fileShare module could not start the server, Try try restarting the jarvis"
            return True

        yield "clear screen"
        for i in result:
            yield str(i)
            yield "\n"

        return True

    # if show file share command is passed
    if(GlobalMethods.isSubStringsList(command , "show file")):

        yield "clear screen"
        
        for i in GlobalData_main.dataListFileShare:
            yield str(i)
            yield "\n"

        return True

    # if troubleshoot command is passed
    if((GlobalMethods.isSubStringsList(command , "troubleshoot")) or (GlobalMethods.isSubStringsList(command , "trouble shoot"))):
        for i in TroubleShooter.startTroubleshooter():
            yield i
        return True

    # if the upload log file command is passed
    if(GlobalMethods.isSubStringsList(command , "upload log file")):
        for i in TroubleShooter.uploadFileAgain():
            yield i
        return True

        
        





























    # if exit all command is passed
    if(GlobalMethods.isSubStringsList(command , "exit all")):
        if(GlobalData_main.isFileShareStarted):
            try:
                FileShareClass.stopFileShare()
            except Exception as e:
                GlobalData_main.objClogger.exception(str(e) , "Exception in closing the file share server at {} while exit all".format(str(FileShareClass.path)))

        sys.exit()


    # if exit command is passed
    if(GlobalMethods.isSubStringsList(command , "exit")):
        if(GlobalData_main.isFileShareStarted):
            yield "could not quit the program, file share is already running, use stop file share to quit it first"
            return True

        sys.exit()


    


    else:
        yield "Command not found , Try again , or Type Help for Help"

























# main function for inputting commands
def main():

    # running until exit is called in driver
    while(True):
        customClearScreen()

        userName = GlobalData_main.settingDict.get("username" , "None")

        if(userName == "None"):
            userName = getpass.getuser()
            GlobalData_main.userCP = "settings = None , PC = " + str(userName)
        else:
            GlobalData_main.userCP = "settings = {} , PC = {}".format(userName , getpass.getuser())


        if(GlobalData_main.toUpgradeJarvis):
            print("New version of jarvis is available, run update jarvis command to download the new version")
            print()

        for i in GlobalData_main.printDataList:
            print(i)
            print()

        # greeting the user
        print("Welcome {} , What can i do for you :)\n".format(userName))

        # inputting the command
        command = input("Enter Command : ")

        customClearScreen()

        # priting the result from driver function
        for i in driver(command):
            if(i == "#take input#"):
                inputted = input(GlobalData_main.tempInputToShow)
                GlobalData_main.tempInput = inputted
            elif(i == "clear screen"):
                customClearScreen()
            else:
                print(i)

        print("\n\nPress Enter to continue ...")
        input()


        




# main main 
if __name__ == "__main__":
    
    multiprocessing.freeze_support()

    # closing the loading animation
    GlobalData_main.runLoadingAnimation = False
    GlobalData_main.lAnimationObj.join()

    # A message will be printed if the troubleshoot value is True by default
    if(GlobalData_main.troubleshootValue):
        print("\nIn dev Mode \n")
        time.sleep(0.5)

    customClearScreen()

    # cache the settings dict in main memory
    try:
        GlobalData_main.settingDict = Settings.returnDict()
    
    # if the cache fails then the settings file retored may not have been written due to not availabilty of cpu
    except Exception as e:
        GlobalData_main.objClogger.exception(str(e) , "Exception in getting the dict from the settings file , may be the cpu was busy , trying again in 1 sec")
        time.sleep(1)

        # after one second jarvis will try again
        try:
            GlobalData_main.settingDict = Settings.returnDict()

            # if jarvis fails this time also then the computer must have been in deadlock state or jarvis does not have read write permission to program's data folder
        except Exception as e:
            GlobalData_main.objClogger.exception(str(e) , "Exception in getting the dict from the settings file , may be the cpu was busy , or jarvis does not have read write permission")
            customClearScreen()
            print("Could not load the settings file , cpu does not responded or jarvis does not have read write permission , Try again in some time :(")
            print("\n\nPress enter to continue")
            input()
            sys.exit()


    # starting the version checker thread
    # once the thread finishes and lastest new version is found then toUpgrade handler will be set to True in global data class which will be picked by the if statement in main function
    versionCheckerObj = versionChecker()
    versionCheckerObj.start()
    
    # creating a driver function reference to be used by troubleshoot class
    GlobalData_main.driverFuncReference = driver

    # main will be called
    main()
