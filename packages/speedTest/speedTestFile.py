import speedtest   





class SpeedTestClass:
    """
This is the main class of speed test file

methods - 
1.  runSpeedTestUtility    ->    this the only method that you need to use this class functions as
                                 this methods automatically calls other methods of the class

                                 this method accepts two arguments -
                                                                                
                                 1st inBytes - if the result shown need to be in MegaBytes instead of Megabits
                                               default value of this is False
                                                                                
                                 2nd numberOfTimesToDo - How many times you need to average the result out
                                                         default value is two
    """

    # contructor for the class
    def __init__(self , objClogger):
        self.st = None
        self.objClogger = objClogger
    

    # function to set things up - mainly creating obj of speedtest module and setting up server
    # this function returns False if it cannot find a serve - mainly due to lack of internet connection
    def setThingsUp(self):
        try:
            # creating object
            self.st = speedtest.Speedtest()

            # getting best server
            self.st.get_best_server()


            self.objClogger.log("server setted up successfully in speed test class set things up function" , "i")

            return True     # returned True as server setted up successfully

        except Exception as e:
            self.objClogger.exception(str(e) , "Exception in setting up the server in speed test class set things up function")
            return False


    # function to convert bits into mega bits
    def convToMb(self , bitsPass):
        return (bitsPass / (1024 * 1024))


    # function to convert mega bits to mega bytes
    def convToMB(self , megaBitsPass):
        return (megaBitsPass / 8)


    # function to get the download speed
    def getDownloadSpeed(self):
        try:
            toReturn = self.st.download()
            self.objClogger.log("download speed checked successfullly in speed test class get download speed function" , "i")
            return toReturn
        except Exception as e:
            self.objClogger.exception(str(e) , "Exception in getting the download speed in speed test class get donwload speed function")
            return False


    # function to get the upload speed
    def getUploadSpeed(self):
        try:
            toReturn = self.st.upload()
            self.objClogger.log("upload speed checked successfullly in speed test class get upload speed function" , "i")
            return toReturn
        except Exception as e:
            self.objClogger.exception(str(e) , "Exception in getting the upload speed in speed test class get upload speed function")
            return False


    # function to get the upload speed
    def getPing(self):
        try:
            toReturn = self.st.results.ping
            self.objClogger.log("ping checked successfullly in speed test class get ping function" , "i")
            return toReturn
        except Exception as e:
            self.objClogger.exception(str(e) , "Exception in getting the ping speed test class get ping function")
            return False


    # main function of the class to handle all the internal process and output result
    def runSpeedTestUtility(self , inBytes = False , numberOfTimesToDo = 2):
        yield "running speed test - this may take some time"
        
        # checking internet connection status
        status = self.setThingsUp()
        
        if(status == False):
            
            # if the internet is not present
            yield "clear screen"
            yield "Could not run speed test , make sure you are online ..."
            return

        else:
            # setting up some variables to avoid garbage value allocation
            avgDownloadSpeed = 0
            avgUploadSpeed = 0
            avgPing = 0
            value = 0

            # running loop for doing number of test as pass or by default 2 times
            for i in range(numberOfTimesToDo):

                # printing message
                yield "clear screen"
                yield "running speed test - this may take some time"
                yield "\nProcessing pass {} out of {}".format(i+1 , numberOfTimesToDo)

                # checking download speed
                yield "\nchecking Download Speed..."

                value = self.getDownloadSpeed()

                if(value == False):
                        yield "clear screen"
                        yield "\nSpeed test failed, Something went wrong, Please Try again, if error persist, run troubleShoot command"
                        return

                avgDownloadSpeed = avgDownloadSpeed + value

                # checking upload speed
                yield "checking Upload Speed..."

                value = self.getUploadSpeed()

                if(value == False):
                    yield "clear screen"
                    yield "\nSpeed test failed, Something went wrong, Please Try again, if error persist, run troubleShoot command"
                    return

                avgUploadSpeed = avgUploadSpeed + value

                # checking ping 
                yield "checking Ping..."

                value = self.getPing()
                if(value == False):
                    yield "clear screen"
                    yield "\nSpeed test failed, Something went wrong, Please Try again, if error persist, run troubleShoot command"
                    return
                    
                avgPing = avgPing + value


            avgDownloadSpeed = avgDownloadSpeed / (numberOfTimesToDo) 
            avgUploadSpeed = avgUploadSpeed / (numberOfTimesToDo)
            avgPing = avgPing / (numberOfTimesToDo)

            avgDownloadSpeed = self.convToMb(avgDownloadSpeed)
            avgUploadSpeed = self.convToMb(avgUploadSpeed)

            yield "clear screen"
            
            if(inBytes == False):
                yield "Download speed    =    {} Mb/s".format(avgDownloadSpeed)
                yield "upload speed      =    {} Mb/s".format(avgUploadSpeed)
                yield "ping              =    {} ms".format(avgPing)
            else:
                yield "Download speed    =    {} MB/s".format(self.convToMB(avgDownloadSpeed))
                yield "upload speed      =    {} MB/s".format(self.convToMB(avgUploadSpeed))
                yield "ping              =    {} ms".format(avgPing)

            self.objClogger.log("speed test main function - run speed test utility executed successfully", "i")

            return



   
if __name__ == "__main__":
    obj = SpeedTestClass()
    obj.runSpeedTestUtility(True)

