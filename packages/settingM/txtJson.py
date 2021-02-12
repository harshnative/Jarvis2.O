class TxtJson:

    # method to get a dict form a txt file
    @classmethod
    def getDict(cls , filePath):
        
        # reading the txt file
        with open(filePath , "r") as file:
            myList = file.readlines()

        myDict = {}

        for i in myList:

            # removing etc spaces and "\n" from i
            i = i.strip()

            # of the i is empty or i[0] is # (for comments) then it will be not added to dict
            if((i != "") and (i[0] != "#")):

                # getting the key 
                key = ""

                dColPos = 0
                
                for num , j in enumerate(i):

                    # if we encounter the : then we can store its pos so that when getting value we do not traverse string form start 
                    if(j == ":"):
                        dColPos = num
                        break

                    key = key + j

                key = key.strip()
                
                value = ""

                # if the value is not present then it will be null
                if(dColPos == 0):
                    value = None
                else:    
                    value =  i[dColPos + 1:]
                    value = value.strip()

                myDict[key] = value
        
        return myDict

    
    # method to write a dict to txt
    @classmethod
    def writeDict(cls , dictObj , filePath , append = False):

        # setting the mode
        if(append):
            mode = "a"
        else:
            mode = "w+"

        firstTime = True

        with open(filePath , mode) as file:
            for i,j in dictObj.items():
                
                # if it is first time the we don't need "\n"
                if(firstTime and not(append)):
                    firstTime = False
                else:
                    file.write("\n\n")
                string = str(i) + "    " + ":" +  "    " + str(j)
                file.write(string)








if __name__ == "__main__":
    
    # print(TxtJson.getDict("hello.txt"))
    

    x = {
    123456 : "boi" ,
    456 : "bye" ,    
    789 : "don" ,
    }

    TxtJson.writeDict(x , "hello.txt")
    print(TxtJson.getDict("hello.txt"))

    TxtJson.writeDict(x , "hello.txt" , True)
    print(TxtJson.getDict("hello.txt"))

