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

    # letscode api key
    lcApiKey = ""

    # key for open weather api
    openWeatherApiKey = ""

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

    # auto complete reference list
    autoCompleteReference = None

    # search reference dict
    searchDict = {'weather': {}, 
                'update': {}, 
                'jarvis': {}, 
                'speed': {}, 
                'test': {}, 
                'setting': {}, 
                'restore': {}, 
                'open': {}, 
                'password': {}, 
                'set': {}, 
                'file': {}, 
                'port': {}, 
                'stop': {}, 
                'start': {}, 
                'share': {},
                '-log': {},
                '-a': {},
                '-d': {},
                'http': {},
                'show': {}, 
                'upload': {}, 
                'log': {}, 
                'troubleshoot': {}, 
                'exit': {}, 
                'all': {},
                '-b': {},
                'add': {},
                'me': {},
                'to': {},
                'root': {},
                'add': {},
                'file': {},
                'to': {},
                'me': {},
                }





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







































# function to reset the logger obj
# necessary when the troubleshoot value is changed
def resetLoggerObj():
    # setting up the logger module
    try:
        GlobalData_main.objClogger = loggerpy.Clogger(GlobalData_main.isOnWindows , GlobalData_main.isOnLinux , GlobalData_main.folderPathWindows_simpleSlash , GlobalData_main.folderPathLinux)
    except PermissionError:
        print("\nPlease run jarvis using sudo")
        sys.exit()

    GlobalData_main.objClogger.setTroubleShoot(GlobalData_main.troubleshootValue)


# setting up logger obj for first time
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
import hjson
import datetime

# for auto completion
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer


# for adv search 
""" bundling it in my packages to resolve the pyinstaller error"""
from packages.fast_autocomplete import AutoComplete


# self made modules
from packages.speedTest import speedTestFile
from packages.settingM import settingsFile
from packages.settingM import txtJson
from packages.passwordStorer import mainCode
from packages.apiStorage import apiStorer



# importting components for file share functionality
from packages.fileShare import FS
from tkinter import filedialog
from tkinter import *

# init tkinter
if __name__ == "__main__":
    GlobalData_main.root = Tk()
    GlobalData_main.root.withdraw()






























# class containing some of the global methods
class GlobalMethods:

    # setting up the adv search obj
    advSearchObj = AutoComplete(words=GlobalData_main.searchDict)



    # method for correcting the incorrect spelling
    @classmethod
    def correctCommand(cls , command):

        # function to find the number of matched characters in two strings
        def matchCharInString(string1 , string2):
            setString1 = set(string1)
            setString2 = set(string2)

            matchedCharacters = setString1 & setString2

            return len(matchedCharacters)


        try:

            # making the command list
            command = str(command)

            commandList = command.split()

            newCommand = ""

            # traversing the command list
            for i in commandList:
                i = str(i).strip()

                # if i starts with - then skip the auto correction function
                # and directly add i to new command
                if(i[0] == "-"):
                    newCommand = newCommand + str(i) + " "
                    continue
                
                # if i is number then skip the auto correction function
                if(i.isnumeric()):
                    newCommand = newCommand + str(i) + " "
                    continue


                # search list from the adv search object
                result = cls.advSearchObj.search(word=i)
                
                # if no result was returned then skip auto correctness
                try:
                    result = result[0]
                    GlobalData_main.objClogger.log("adv search found result[0] in result in Globalmethods class correctCommad function with result = {} and searchString = {}".format(result , i) , "i")

                except IndexError:
                    newCommand = newCommand + i + " "
                    GlobalData_main.objClogger.log("adv search Index error in Globalmethods class correctCommad function with result = {} and searchString = {}".format(result , i) , "i")
                    continue


                # if result contains more than 1 string then simply add old command
                # which means we are not able to determine the exact command
                # as program can cannot determine the exact command
                if(len(result) != 1):
                    newCommand = newCommand + i + " "
                    GlobalData_main.objClogger.log("adv search found multiple items in result in Globalmethods class correctCommad function with result = {} and searchString = {}".format(result , i) , "i")

                
                # if the result contains length difference of more than 2 then it means program may as huge difference in command entered and corrected command which may not be exact command
                # as returning some other result may lead to execution of command which was not intended
                # so to prevent running of command not usaully entered we skip this correctness
                elif(not(abs(len(result[0]) - len(i)) <= 2)):
                    newCommand = newCommand + i + " "
                    GlobalData_main.objClogger.log("adv search result items differ from i way to much in terms of length in Globalmethods class correctCommad function with result = {} and searchString = {}".format(result , i) , "i")

                # if the number characters in the string differ by lot , then also skip correction
                elif(not(abs(matchCharInString(result[0] , i) - len(set(i))) <= 2)):
                    newCommand = newCommand + i + " "
                    GlobalData_main.objClogger.log("adv search result items differ from i way to much in Globalmethods class correctCommad function with result = {} and searchString = {}".format(result , i) , "i")

                # else we correct this command
                else:
                    newCommand = newCommand + str(result[0]) + " "
                    GlobalData_main.objClogger.log("adv search successfully replaced the mispelled command in Globalmethods class correctCommad function with result = {} and searchString = {}".format(result , i) , "i")


            return newCommand

        # if some error occur simply return the old command
        except Exception as e:
            GlobalData_main.objClogger.exception(str(e) , "Exception in Globalmethods class correctCommad function with command = {}".format(command))
            return command



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

        string = str(string)
        subString = str(subString)

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






















# function to set the apis from the local storage to keep them safe
def setApis():
    GlobalData_main.lcApiKey = apiStorer.StorageClass.letsCodeApi
    GlobalData_main.openWeatherApiKey = apiStorer.StorageClass.openWeatherApi


if __name__ == "__main__":
    # setting up the api
    setApis()

    tempList = []
    # converting search dict keys to list
    for i,j in GlobalData_main.searchDict.items():
        tempList.append(i) 

    # setting up values in auto completer
    GlobalData_main.autoCompleteReference = WordCompleter(tempList, ignore_case=True)



























# class to get the wheather details
class WeatherFunctionality:
    
    def __init__(self):
        
        # making the object
        self.moduleObj = owm.WeatherDataClass()

        # set the api key here
        # it is removed before commiting for security reasons
        self.__apiKey = GlobalData_main.openWeatherApiKey

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

            # if the retruned dict length is zero then restore the settings file
            if(len(returnedDict) == 0):
                cls.restoreSettings()
                time.sleep(0.5)

            GlobalData_main.objClogger.log("settings dict returned successfully in returnDict function in settings class with dict = {}".format(returnedDict) , "i")
            return returnedDict

        except Exception as e:
            GlobalData_main.objClogger.exception(str(e) , "error in settingObj.getDict() function")
            return {}

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

    # path to the folder to share
    path = None 

    
    # function to set the share path for the file share
    # if the path passed is None or incorrect then 
    # open the tk gui window and then stores the returned path in class var
    # return False if process fails else return True
    @classmethod
    def setSharePath(cls , path = None):
        try:

            # check the path passed if it is not None
            if(path != None):
                if(os.path.exists(str(path)) == True):
                    folder_selected = path

                # if the path is incorrect simply open the gui window
                else:
                    folder_selected = filedialog.askdirectory()
            
            else:
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
    def startFileShare(cls , http = False , anomus = False , logToConsole = False):
        GlobalData_main.dataListFileShare.clear()

        try:

            # getting the user name and password for file share in settings file
            userName = GlobalData_main.settingDict.get("userName_fileShare" , "None")
            if(str(userName).lower() == "none"):
                userName = "user"
            
            userPass = GlobalData_main.settingDict.get("password_fileShare" , "None")
            if(str(userPass).lower() == "none"):
                userPass = "147896"

            # if log to console is not active
            if(not(logToConsole)):

                # start the file share with parameters
                for i in cls.fil.start_fileShare(cls.path , http=http , port=GlobalData_main.portForFileShare , useOtherPort=True , userNameFTP=userName , userPasswordFTP=userPass , FTPanomusAccess=anomus , logToConsole=False):
                    # add returned data to global data list
                    if(i != None):
                        GlobalData_main.dataListFileShare.append(i)

                # add details to global data for quick message before enter command function 
                GlobalData_main.addressForShare = cls.fil.get_ip_address()
                GlobalData_main.printDataList.append("File Share active at {}:{}".format(str(GlobalData_main.addressForShare) , str(cls.fil.getPort())))
                GlobalData_main.objClogger.log("file share server started at {}".format(str(cls.path)) , "i")
                GlobalData_main.isFileShareStarted = True
                return GlobalData_main.dataListFileShare
            
            # if we need to log to screen
            else:
                customClearScreen()

                # then start file share and print details
                for i in cls.fil.start_fileShare(cls.path , http=http , port=GlobalData_main.portForFileShare , useOtherPort=True , userNameFTP=userName , userPasswordFTP=userPass , FTPanomusAccess=anomus , logToConsole=True):
                    if(i != None):
                        print(i)
                        print()

                # when the key board interupt will happend it will go to retrun [] at last

                               

        except Exception as e:
            GlobalData_main.objClogger.exception(str(e) , "Exception in starting the file share server at {}".format(str(cls.path)))
            return None
        
        return ["file sharing stopped"] 

    
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
































class VersionChecker(Thread):

    def run(self):
        try:

            # getting the response from website api
            response = requests.post("https://www.letscodeofficial.com/jarvis_version" , data={"key" : GlobalData_main.lcApiKey}).json()
            
            # reponse is like [{"version": 0.1}] so getting the dict from index 0
            dictResponse = response[0]

            currentVersion = GlobalData_main.currentVersion
            versionFromResponse = dictResponse.get('version')

            # comparing the versions
            if(versionFromResponse > currentVersion):
                GlobalData_main.toUpgradeJarvis = True

            GlobalData_main.objClogger.log("jarvis new version thread runned succesfully with version from response = {} and current version = {}".format(str(versionFromResponse) , str(currentVersion)) , "i")

            return versionFromResponse

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
            response = requests.post('https://letscodeofficial.com/upload_jarvisLog/' , files={"file": logFile} , data={"key" : GlobalData_main.lcApiKey , "remark" : str(GlobalData_main.userCP + " upload on {}".format(str(datetime.datetime.now())))})
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
            yield "\n\nTrouble shoot aborted..."
            return

        # we need to make user re run the command when the troubleshoot value was not enabled by default
        # else we just need to upload the log file
        if(not(GlobalData_main.troubleshootValue)):

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

            try:
                # priting the result from driver function
                for i in GlobalData_main.driverFuncReference(command):
                    yield i
            except Exception as e:
                GlobalData_main.objClogger.exception(str(e) , "Exception noted while running troubleshooter command")


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

    # correcting the command - slighty mispelled commands will be corrected to correct command
    command = GlobalMethods.correctCommand(command)

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
        customPath = GlobalData_main.settingDict.get("path_for_password_db")


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

        path = None

        # if -d is passed
        if(GlobalMethods.isSubStringsList(command , "-d")):
            path = GlobalData_main.settingDict.get("defaultFolderFileShare" , "None")
            if(str(path).lower() == "none"):
                path = None


        status = FileShareClass.setSharePath(path=path)

        if(not(status)):
            yield "fileShare module could not get path, Try again"
            return True

        http = False
        logToConsole = False
        anomus = False

        # if http is passed in command
        if(GlobalMethods.isSubStringsList(command , "http")):
            http = True
        
        # if -log is passed in command
        if(GlobalMethods.isSubStringsList(command , "-log")):
            logToConsole = True
        
        # if -a is passed in command
        if(GlobalMethods.isSubStringsList(command , "-a")):
            anomus = True

        # call the function and pass parameters
        result = FileShareClass.startFileShare(http=http , logToConsole=logToConsole , anomus=anomus)

        if(result == None):
            yield "fileShare module could not start the server, Try try restarting the jarvis"
            return True

        yield "clear screen"
        for i in result:
            yield str(i)
            yield "\n"

        return True



    # if add file to me command is passed
    if(GlobalMethods.isSubStringsList(command , "add file me")):

        # only for linux users
        if(GlobalData_main.isOnWindows):
            yield "This feature is only for linux users"

        elif(GlobalData_main.isOnLinux):
        
            # getting the user name to which ownership be added
            userName = "None"

            if(GlobalMethods.isSubStringsList(command , "-d")):
                userName = GlobalData_main.settingDict.get("defaultUserName" , "None")

            if(userName == "None"):
                # accepting the user aggrement to data share
                resetTempInput()
                GlobalData_main.tempInputToShow = "\n\nEnter the userName to add ownership of file share , you can see your user name by running whoami command , you can also add your user name to settings file and run with -d option : "
                yield "#take input#"
                userName = GlobalData_main.tempInput
                resetTempInput()
            
            # if no path is present in file share memory prompt 
            if(FileShareClass.path == None):
                yield "clear screen"
                yield "file share module could not find the path to dir"
                yield "you can run this command instead the dir were you started file share manaully - "
                yield "sudo chown -R {} *".format(userName)

                return True

            # add ownership
            os.system("sudo chown -R {} {}/*".format(userName , FileShareClass.path))

            
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


















    # if the add me to root command is passed
    if(GlobalMethods.isSubStringsList(command , "add me to root")):
        
        if(GlobalData_main.isOnWindows):
            yield "This feature is only for linux users"

        elif(GlobalData_main.isOnLinux):
            yield "add this line to end in file opened - "
            yield "\nusername ALL = (root) NOPASSWD: /bin/jarvis"
            yield "\njust replace username with your your name , you can find your username by running whoami command\n"

            os.system("sudo gedit /etc/sudoers")

            yield "clear screen"

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


    session = PromptSession(completer=GlobalData_main.autoCompleteReference)


    # running until exit is called in driver
    while(True):
        customClearScreen()


        # getting the user name from the settings file
        userName = GlobalData_main.settingDict.get("userName" , "None")


        # if username in the settings file is None then username of operating system will be used
        if(userName == "None"):
            userName = getpass.getuser()
            GlobalData_main.userCP = "settings = None , PC = " + str(userName)
        else:
            GlobalData_main.userCP = "settings = {} , PC = {}".format(userName , getpass.getuser())


        # if new version of jarvis is available then prompt
        if(GlobalData_main.toUpgradeJarvis):
            print("New version of jarvis is available, run update jarvis command to download the new version")
            print()

        # if some child process of jarvis is running prompt
        for i in GlobalData_main.printDataList:
            print(i)
            print()

        # greeting the user
        print("Welcome {} , What can i do for you :)\n".format(userName))

        # inputting the command
        # command = input("Enter Command : ")
        command = session.prompt('Enter Command : ')

        customClearScreen()

        # priting the result from driver function
        for i in driver(command):

            # global take input
            if(i == "#take input#"):
                inputted = input(GlobalData_main.tempInputToShow)
                GlobalData_main.tempInput = inputted

            # if function wants to clear screen
            elif(i == "clear screen"):
                customClearScreen()

            # else print output
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

    
    # check for the LC api key and print a message if not setted up
    if((GlobalData_main.lcApiKey == None) or (GlobalData_main.lcApiKey == "")):
        print("lets code api key not setted")
        time.sleep(0.7)


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
    versionCheckerObj = VersionChecker()
    versionCheckerObj.start()

    # getting the dict from the settings file
    resultFromDict = GlobalData_main.settingDict.get("accept_user_experience_program" , "False")


    # promt user to participate in the user experience program
    if(resultFromDict.lower() == "none"):
        customClearScreen()
        print("Want to participate in user experience program ?")
        print("It will help in resolving errors later.")
        print("logger object will log at info level but no sensitive information is ever logged")
        inputtedValue = input("\nEnter 1 to accept , anything else to reject : ")
        if(inputtedValue == "1"):
            GlobalData_main.settingDict["accept_user_experience_program"] = "True"
        else:
            GlobalData_main.settingDict["accept_user_experience_program"] = "False"

        settingsPath = Settings.settingObj.path
        with open(settingsPath , "w+") as file:
            file.write(hjson.dumps(GlobalData_main.settingDict))



    # checking if the user agree to the user expreince program
    if((resultFromDict.lower() == "true") and (not(GlobalData_main.troubleshootValue))):
        GlobalData_main.troubleshootValue = True
        resetLoggerObj()

    # if the script is runned
    elif(GlobalData_main.troubleshootValue):
        print("\nIn Dev Mode \n")
        time.sleep(0.2)


    # creating a driver function reference to be used by troubleshoot class
    GlobalData_main.driverFuncReference = driver


    # A message will be printed if the troubleshoot value is True by default
    if(GlobalData_main.troubleshootValue):
        print("\nIn UEP Mode \n")
        time.sleep(0.2)

    # main will be called
    main()


