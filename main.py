# essential modules
import os
import platform
import time
import sys
import subprocess as sp
from threading import Thread
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
from packages.logger import loggerpy 




# declaring some global variables
class GlobalData_main:

    # variables to determine the operating system of the user 
    isOnWindows = False
    isOnLinux = False

    # variables to manage the loading animation 
    runLoadingAnimation = True
    loadingAnimationCount = 5
    lAnimationObj = None


    # path for storing the program files
    folderPathWindows = r"C:\programData\JarvisData"
    folderPathLinux = os.getcwd() + "/JarvisData"
    folderPathWindows_simpleSlash = r"C:/programData/JarvisData"

    # obj for logger module
    objClogger = None
    troubleshootValue = True

    # dict from the settings file will be stored here
    settingDict = None 







# Checking the users operating system and adding data to global class
osUsing = platform.system()

if(osUsing == "Linux"):
    GlobalData_main.isOnLinux = True

    # making the program data folder
    try:
        os.mkdir(GlobalData_main.folderPathLinux)
    except FileExistsError:
        pass

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
        os.system("self")
    else:
        sp.call('clear',shell=True)



# setting up the logger module
GlobalData_main.objClogger = loggerpy.Clogger(GlobalData_main.isOnWindows , GlobalData_main.isOnLinux , GlobalData_main.folderPathWindows_simpleSlash , GlobalData_main.folderPathLinux)
GlobalData_main.objClogger.setTroubleShoot(GlobalData_main.troubleshootValue)





# loading animation thread
class LoadingAnimation(Thread):

    def run(self):

        customClearScreen()
        string = ""

        # will run only till max 5 times or early if the global var runLoadingAnimation is made false
        while(GlobalData_main.runLoadingAnimation and GlobalData_main.loadingAnimationCount):
            string = string + "."
            time.sleep(0.5)
            print("\rloading , please wait " , string , sep = "" , end = "")
            GlobalData_main.loadingAnimationCount -= 1

        print()






# starting in the main to avoide awakeness by sub processes
if __name__ == "__main__":

    # loading animation thread started 
    GlobalData_main.lAnimationObj = LoadingAnimation()
    GlobalData_main.lAnimationObj.start()








# importing additional modules
from easyOpenWeather import module as owm
from tabulate import tabulate

from packages.speedTest import speedTestFile
from packages.settingM import settingsFile





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
        self.__apiKey = ""

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
        returnedDict = cls.settingObj.getDict()
        return returnedDict

    # method to open the settings file
    # returns True on successfull opening 
    # else returns false and logs error
    @classmethod
    def openSettingsFile(cls):
        result = cls.settingObj.openSettings()

        if(result == None):
            return True
        else:
            GlobalData_main.objClogger.exception(str(result) , "Exception in opening the settings file")
            return False



# main driver function for executing commands
def driver(command):

    """No print is used before main to keep the functions modular , just return the result to main in list form or yield form"""
    

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
            return

        # else if city is not passed then it will be taken from the settings file
        elif((len(cityName) <= 1)):
            cityName = cityNameFromSet
            

        # getting the result from the class
        weatherObj = WeatherFunctionality()

        result = weatherObj.returnDataDict(cityName)

        # if the api key is not set then return the message
        if(result == None):
            yield "please set the api key"
            return
        
        if(result == "error"):
            yield "please pass a correct city name"
            return

        # else conv the dict returned into list with [[key] , [value]]
        resultList = []

        for i , j in result.items():
            tempList = []
            tempList.append(i)
            tempList.append(j)
            resultList.append(tempList)

        # using the tabulate module to pretify the output
        toReturn = tabulate(resultList , headers=['Query', 'Data'])

        # returning the result so it can be printed
        yield toReturn


    # if the speed test  command is passed
    if(GlobalMethods.isSubStringsList(command , "speed test")):
        sObj = speedTestFile.SpeedTestClass(GlobalData_main.objClogger)

        for i in sObj.runSpeedTestUtility():
            yield i
        
        return

    # if the setting command is passed
    if(GlobalMethods.isSubStringsList(command , "setting")):
        if(Settings.openSettingsFile()):
            yield "Settings file opened"
            yield "\nDon't forget to save it and run the update command after wards"
            return
        else:
            yield "Error opening the settings file , Try running the troubleshoot command"
            return

    
    # if exit command is passed
    if(GlobalMethods.isSubStringsList(command , "exit")):
        sys.exit()


    else:
        yield "Command not found , Try again , or Type Help for Help"




# main function for inputting commands
def main():

    # running until exit is called in driver
    while(True):
        customClearScreen()

        userName = GlobalData_main.settingDict.get("username" , "sir")

        # greeting the user
        print("Welcome {} , What can i do for you :)\n".format(userName))

        # inputting the command
        command = input("Enter Command : ")

        customClearScreen()

        # priting the result from driver function
        for i in driver(command):
            if(i == "clear screen"):
                customClearScreen()
            else:
                print(i)

        print("\n\nPress Enter to continue ...")
        input()


        




# main main 
if __name__ == "__main__":

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


    # main will be called
    main()
