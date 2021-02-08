# declaring some global variables
class GlobalData_main:
    
    # if the troubleshoot is enabled or not
    troubleshoot = False

    # variables to determine the operating system of the user 
    isOnWindows = False
    isOnLinux = False

    # variables to manage the loading animation 
    runLoadingAnimation = True
    loadingAnimationCount = 5
    lAnimationObj = None









# essential modules
import os
import platform
import time
import sys
import subprocess as sp
from threading import Thread










# Checking the users operating system and adding data to global class
osUsing = platform.system()

if(osUsing == "Linux"):
    GlobalData_main.isOnLinux = True
elif(osUsing == "Windows"):
    GlobalData_main.isOnWindows = True
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
                        return True
                    else:
                        pass
            return False
        except Exception as e:
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












class WeatherFunctionality:
    
    def __init__(self):
        self.moduleObj = owm.WeatherDataClass()
        self.moduleObj.setApiKey("")
    
    def returnDataDict(self , cityName):
        self.moduleObj.setCityName(cityName)
    
        listPass = ["tempInC" , "tempMin" , "tempMax" , "pressure" , "humidity" , "windSpeed" , "windDirection" , "clouds" , "description"]

        self.moduleObj.setList(listPass)
        return self.moduleObj.getInfo()




def driver(command):
    

    if(GlobalMethods.isSubStringsList(command , "weather")):
        print("hello")




def main():

    while(True):
        customClearScreen()

        print("Welcome sir , What can i do for you :)\n")

        command = input("Enter Command : ")

        driver(command)

        input()

        




# main main 
if __name__ == "__main__":

    # closing the loading animation
    GlobalData_main.runLoadingAnimation = False
    GlobalData_main.lAnimationObj.join()

    main()
