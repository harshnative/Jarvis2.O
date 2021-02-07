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
        os.system("cls")
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




# main main 
if __name__ == "__main__":

    # closing the loading animation
    GlobalData_main.runLoadingAnimation = False
    GlobalData_main.lAnimationObj.join()

    print("end")

