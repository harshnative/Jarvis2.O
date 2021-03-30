import subprocess as sp
import os
import stdiomask
from .eSqlite import SQLiteConnect
import sys
import pandas as pd
import pyperclip
import time


# function to input password in hash form
def hashPasswordInput(message):
    password = stdiomask.getpass(message)
    return password




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
                        return True
                    else:
                        pass

            # logging the result for debugging purpose
            return False

        except Exception as e:

            # logging the error
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







# main class of module
class PasswordStorerClass:

    def __init__(self , isOnWindows , isOnLinux , folderPathWindows_simpleSlash , folderPathLinux , customDbPath = None):

        # if the custom path is passed the use it
        if(customDbPath != None):
            self.DataBasePath = customDbPath
        

        else:
            # data base name
            self.dataBaseName = "jarvisPassDB.db"

            # setting the actaul path with name
            if(isOnWindows):
                self.DataBasePath = folderPathWindows_simpleSlash + "/" + self.dataBaseName
            elif(isOnLinux):
                self.DataBasePath = folderPathLinux + "/" + self.dataBaseName

        self.isOnWindows = isOnWindows

        # table name for db
        self.tableNameForDB = "pass table"

        # self data base db
        self.dbObj = SQLiteConnect()
    


    # clear screen function 
    def customClearScreen(self):
        if(self.isOnWindows == True):
            os.system("cls")
        else:
            sp.call('clear',shell=True)



    # function to find whether a word is present in string or not
    def isSubString(self , string , subString):
        try:
            lengthOfSubString = len(subString)
            for i,j in enumerate(string):
                if(j == subString[0]):
                    if(subString == string[i:i+lengthOfSubString]):
                        return True 
                    else:
                        pass
            return False
        except Exception as e:
            return False

    

    # main function , just invoke this after setting up the parameter to use this module
    def driverFunc(self):


        # setting up the data base in eSqlite module obj
        self.dbObj.setDatabase(self.DataBasePath)

        self.customClearScreen()


        # if the data base exist and their is already password setted in it
        # then just input password from user and verify
        # if password verfiy then set it to eSqlite obj for encryption and decryption
        if(self.dbObj.checkForPasswordTable()):

            # try to re - enter the password till its correct
            while(True):
                    print()
                    password = hashPasswordInput('enter password : ')
                    pin = 0
                    try:
                        pin = int(hashPasswordInput("enter pin : "))
                    except Exception:
                        print("\n\nPin should only consist of numbers...")
                        input("\npress enter to continue...")
                        self.customClearScreen()
                        continue

                    status = self.dbObj.setPassword(password , pin)

                    if(status):
                            self.dbObj.setSecurityStatus(True)
                            del password
                            del pin
                            break
                    else:
                            print("\n wrong password")
                            input("\n\nPress Enter to continue")
                            self.customClearScreen()


        # else ask for new password and generate a password table in db using eSqlite obj
        else:
            
            while(True):
                self.customClearScreen()
                print()
                password = hashPasswordInput('enter new password : ')
                pin = 0
                try:
                    pin = int(hashPasswordInput("enter new pin : "))
                except Exception:
                    print("\n\nPin should only consist of numbers...")
                    input("\npress enter to continue...")
                    continue

                
                print()

                password1 = hashPasswordInput('enter password again : ')
                pin1 = 0
                try:
                    pin1 = int(hashPasswordInput("enter pin again : "))
                except Exception:
                    print("\n\nPin should only consist of numbers...")
                    input("\npress enter to continue...")
                    continue

                if((password != password1) and (pin != pin1)):
                        print("\nPassword and pin does not match")
                else:
                        status = self.dbObj.setPassword(password , pin)
                        if(status == None):
                                break
                        else:
                                print("\nsome error occur")


        # create a table with two col data and pass , no exception will be raised if table already exsist
        contentList = [["data" , "TEXT" , 0] , ["pass" , "TEXT" , 0]]
        self.dbObj.createTable(self.tableNameForDB , contentList)

        self.dbObj.setSecurityStatus(True)



        # intialising main operations after setting up things
        # to break while loop exit command will be used 
        # using infinite loop to ensure continue usage of commands 
        while(1):
            self.customClearScreen()

            command = input("Enter command for password manager : ")

            command = command.lower()

            if(command.strip() == "exit"):
                break

            if(command.strip() == "exit all"):
                sys.exit()
            

            self.executeCommand(command)



    # function to display all data in db
    def displayAll(self , all=False):
        if(all):
            self.dbObj.printData()
        else:
            data = self.dbObj.returnData()
            indexList = []
            dataList = []
            for i in data[1:]:
                indexList.append(i[0])
                dataList.append(i[1:])

            pd.set_option("display.max_rows", None)
            pd.set_option("display.max_colwidth", int((os.get_terminal_size()[0]/2) - 5))
            dataFrame = pd.DataFrame(dataList , columns=["reference" , "password"] , index=indexList)
            dataFrame.index.name = "ID"
            print(dataFrame)


    # function to interpret the command and exceute it
    def executeCommand(self , command):

        command = str(command.strip())

        # if the -a or add command is passed
        if((GlobalMethods.isSubStringsList(command , "-a")) or (GlobalMethods.isSubStringsList(command , "add"))):
            self.customClearScreen()

            # input the data in data col and data in pass col 
            data = input("Enter the website name for reference : ")
            password = input("Enter the password : ")

            # if the user by mistake enter the command then pressing enter enter in above input will not lead to insertion in db
            if((data == "") or (password == "")):
                input("\nAdding process cancelled by user , press enter to continue")
                return


            # inserting into table
            valuesList = [data , password]
            self.dbObj.insertIntoTable(valuesList=valuesList)

            input("\nAdded successfully ...")


        # if -sa or see all command is passed
        elif((GlobalMethods.isSubStringsList(command , "-sa")) or (GlobalMethods.isSubStringsList(command , "see all"))):
            self.customClearScreen()
            
            if(GlobalMethods.isSubStringsList(command , "all")):
                self.displayAll(True)
            else:
                self.displayAll()

            index = input("\n\nEnter index number to copy password or Enter to continue : ")

            if(index == ""):
                return
            
            try:
                index = int(index)
            except ValueError:
                print("\n\nWrong index number...")
                time.sleep(0.9)
                return

            data = self.dbObj.returnDataOfKey(index)

            if(data == None):
                print("\n\nWrong index number...")
                time.sleep(0.9)
                return
            
            try:
                pyperclip.copy(data[0][2])
            except NotImplementedError:
                print("\n\nJarvis could not find the copy paste mechanism on your machine.")
                print("This happens with linux users , you will need to install copy paste mechanism")
                print("On Ubuntu/debain you can install it via sudo apt-get install xclip")
                print("If this error occurs on windows , try updating the windows")
                input("\n\nPress enter to continue...")
                return

            print("\n\nPassword copied to clipboard...")
            time.sleep(0.9)


            




        # if -u or update command is passed
        elif((GlobalMethods.isSubStringsList(command , "-u")) or (GlobalMethods.isSubStringsList(command , "update"))):
            self.customClearScreen()

            if(GlobalMethods.isSubStringsList(command , "all")):
                self.displayAll(True)
            else:
                self.displayAll()

            key = 0

            # ask for the index no to update from list show by the above display all function
            try:
                key = int(input("\nEnter the index to update : "))
            except Exception:
                print("\nplease enter valid index no")
                return


            self.customClearScreen()

            # display the data at the key = index no entered
            try:
                self.dbObj.printDataOfKey(key)
            except Exception:
                print("\nplease enter valid index no")
                return


            # get new pass from user and update into db using eSqlite module
            newPass = input("\nEnter new password for above website : ")

            self.dbObj.updateRow("pass" , newPass , key)

            print("\npassword updated successfully")

            input("\npress enter to continue")



        # if the delete command or -d is passed
        elif((GlobalMethods.isSubStringsList(command , "-d")) or (GlobalMethods.isSubStringsList(command , "delete"))):

            if(GlobalMethods.isSubStringsList(command , "all")):
                self.displayAll(True)
            else:
                self.displayAll()

            key = 0


            # ask for the index number to delete
            try:
                key = int(input("\nEnter the index to delete : "))
            except Exception:
                print("\n please enter valid index no")
                return

            self.customClearScreen()

            try:
                self.dbObj.printDataOfKey(key)
            except Exception:
                print("\nplease enter valid index no")
                return


            # confirm from the user to delete the website
            temp = input("\nabove website is going to be deleted , enter 1 to continue or anything else to skip : ")

            if(temp == "1"):
                self.dbObj.deleteRow(key , updateId=True)

                print("\ndeleted successfully")

                input("\npress enter to continue")

            else:
                print("\noperation cancelled")

                input("\npress enter to continue")


        # if the see or -s command is passed
        elif((GlobalMethods.isSubStringsList(command , "-s")) or (GlobalMethods.isSubStringsList(command , "see"))):
            self.customClearScreen()


            # take the search term from the user
            searchTerm = input("Enter a search keyword for search the website : ")


            # get the data from the db
            returnedData = self.dbObj.returnData()

            printList = []


            # search for the data in db and add to list if matches
            for i in returnedData[1:]:
                
                if(self.isSubString(i[1] , searchTerm)):
                    printList.append(i)

            print("\n")


            # display the areas were the data matches
            self.dbObj.tabulatePrinter(printList , returnedData[0])

            index = input("\n\nEnter index number to copy password or Enter to continue : ")

            if(index == ""):
                return
            
            try:
                index = int(index)
            except ValueError:
                print("\n\nWrong index number...")
                time.sleep(0.9)
                return

            data = self.dbObj.returnDataOfKey(index)

            if(data == None):
                print("\n\nWrong index number...")
                time.sleep(0.9)
                return
            
            try:
                pyperclip.copy(data[0][2])
            except NotImplementedError:
                print("\n\nJarvis could not find the copy paste mechanism on your machine.")
                print("This happens with linux users , you will need to install copy paste mechanism")
                print("On Ubuntu/debain you can install it via sudo apt-get install xclip")
                print("If this error occurs on windows , try updating the windows")
                input("\n\nPress enter to continue...")
                return

            print("\n\nPassword copied to clipboard...")
            time.sleep(0.9)


        # if -c or change password command is passed
        elif((GlobalMethods.isSubStringsList(command , "-c")) or (GlobalMethods.isSubStringsList(command , "change password"))):

            oldPass = ""
            oldPin = 123456
            
            while(True):

                # take the old password from user
                self.customClearScreen()
                oldPass = hashPasswordInput("Enter old password : ")
                try:
                    oldPin = int(hashPasswordInput("Enter old pin : "))
                except Exception:
                    print("\nenter valid pin , press enter to continue")
                    input()
                    return


                # check if the password entered is correct using eSqlite module
                status = self.dbObj.setPassword(oldPass , oldPin)

                if(status):
                        self.dbObj.setSecurityStatus(True)
                        break
                else:
                        print("\n wrong password")
                        input()

            password = ""
            pin = 123456


            # if the password entered is correct then proceed
            while(True):

                self.customClearScreen()
                print()

                # ask for new password
                password = hashPasswordInput('enter new password : ')
                pin = 0
                try:
                    pin = int(hashPasswordInput("enter new pin : "))
                except Exception:
                    print("\n\nPin should only consist of numbers...")
                    input("\npress enter to continue...")
                    continue

                
                print()

                password1 = hashPasswordInput('enter password again : ')
                pin1 = 0
                try:
                    pin1 = int(hashPasswordInput("enter pin again : "))
                except Exception:
                    print("\n\nPin should only consist of numbers...")
                    input("\npress enter to continue...")
                    continue

                if((password != password1) and (pin != pin1)):
                        print("\nPassword and pin does not match")
                else:
                        break

            # take a backup of existing passwords in db
            returnedData = self.dbObj.returnData()
            
            try:

                # change the password using eSqlite module
                self.dbObj.changePassword(oldPassword=oldPass , newPassword=password , oldPin=oldPin , newPin=pin)
                print("\npassword changed successfully")
                input("\npress enter to continue ...")
                return
            except Exception as e:

                # if some error occur during the password change
                print("\n error while changing password with exception =  {} , restoring current password ...".format(e))
                
                # delete the corrupted table
                self.dbObj.delEntireTable()

                # restore the old table
                contentList = [["data" , "TEXT" , 0] , ["pass" , "TEXT" , 0]]
                self.dbObj.createTable(self.tableNameForDB , contentList)

                self.dbObj.setSecurityStatus(True)

                for i in returnedData[1:]:
                    self.dbObj.insertIntoTable(valuesList=i[1:])
                
                input("\n press enter to continue")
                return 


        # if command does not matches
        else:
            self.customClearScreen()
            print("wrong command , try -a , -s , -sa , -c , -d , -u , exit , exit all instead..")
            input("\n\npress enter to continue...")



        



            


