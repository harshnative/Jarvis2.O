# importing inbuilt python http server
import http.server
from socket import error, setdefaulttimeout
import socketserver
from contextlib import closing

import os
import socket , errno
from os import path
import multiprocessing
import sys
from importlib import reload

import logging
from pyftpdlib.log import config_logging

# importing FTP module
from pyftpdlib import servers
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.authorizers import DummyAuthorizer



# child class to stop logging of http server
class quietServer(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


# main module class 
class FileShareClass:

	# default constructor 
    def __init__(self):
        self.ipAddress = None
        self.port = 8000
        self.folderToShare = None
        self.mulProcess1 = multiprocessing.Process(target=self.startServerAtFolderSettedHTTP)
        self.mulProcess2 = multiprocessing.Process(target=self.startServerAtFolderSettedFTP)
        self.http = False
        self.logToConsole = True


    # method to set the custom port number
    # raises exception if not a four digit integer
    def setPort(self , port , useOtherPort = False):

        # if wrong port number is not integer type
        try:
            self.port = int(port)
        except Exception:
            raise Exception("Port number passed is not an integer")

        # if port number is not four digit long
        if(1000 < self.port < 10000):
            pass
        else:
            raise Exception("port number must be a four digit integer")
        

        # checking if the port number passed is free or not
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # checking if port binds
        try:
            s.bind((self.ipAddress, self.port))

        # if port does not bind it means that port is not free
        except socket.error as e:
            if(e.errno == errno.EADDRINUSE):

                try:
                    # you don't care just listen to that port
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind((self.ipAddress, self.port))
                except Exception as e:

                    # if using other port is allowed
                    if(useOtherPort):

                        # finding free port by assign port = 0 then system will auto bind the port
                        with closing(s) as s:
                            s.bind(('', 0))
                            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                            
                            # assign the port to object
                            self.port = s.getsockname()[1]
                        
                    # else raise error
                    else:
                        raise RuntimeError("Port {} is already in use".format(self.port))
            
            else:
                pass
            
            s.close()


    # function to get the port number
    def getPort(self):
        return self.port

    # function to set the path to folder to share
    def setSharePath(self , folderPath):

        # if the path passed is incorrect raise error
        if(path.exists(str(folderPath)) == True):
            self.folderToShare = str(folderPath)
        else:
            raise Exception("python cannot find passed folder path to share")

    # function to get the path to folder to share
    def getSharePath(self):
        return self.folderToShare

    # function to get the ip address to the network to which computer is currently connected
    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]


    # function to start the python http server
    # this function does not produce any log messages
    # this function is started has a child process
    def startServerAtFolderSettedHTTP(self):

        # check if ip address and folder share are setted
        if(self.ipAddress == None):
            raise Exception("Could not get system IP Address")
        if(self.folderToShare == None):
            raise Exception("path to folder to share is not setted")    


        # set and start the server
        web_dir = os.path.join(self.folderToShare)
        os.chdir(web_dir)
        
        with socketserver.TCPServer(("", self.port), quietServer) as httpd:
            httpd.serve_forever()


    # function to start the python http server
    # this function will not be started as a child process and will log messages to console
    def startServerAtFolderSettedHTTP_log(self):
        if(self.ipAddress == None):
            raise Exception("Could not get system IP Address")
        if(self.folderToShare == None):
            raise Exception("path to folder to share is not setted")    

        web_dir = os.path.join(self.folderToShare)
        os.chdir(web_dir)
        
        Handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(("", self.port), Handler)

        # this server need to be stopped by Keyboard interrupt 
        httpd.serve_forever()


    # function to start the python ftp server
    def startServerAtFolderSettedFTP(self):
        if(self.ipAddress == None):
            raise Exception("Could not get system IP Address")
        if(self.folderToShare == None):
            raise Exception("path to folder to share is not setted")    


        # Instantiate a dummy authorizer for managing 'virtual' users
        authorizer = DummyAuthorizer()

        # Define a new user having full r/w permissions and a read-only
        # anonymous user
        authorizer.add_user(self.userNameFTP, self.userPasswordFTP, self.folderToShare , perm='elradfmwMT')
        
        if(self.FTPanomusAccess):
            authorizer.add_anonymous(homedir=self.folderToShare)

        # Instantiate FTP handler class
        handler = FTPHandler
        handler.authorizer = authorizer

        config_logging(level=logging.ERROR)

        # Define a customized banner (string returned when client connects)
        handler.banner = "pyftpdlib based ftpd ready."
        address = (self.ipAddress, self.port)  # listen on every IP on my machine on port 21
        server = servers.FTPServer(address, handler)
        server.serve_forever()


    # function to start the python ftp server
    def startServerAtFolderSettedFTP_log(self):
        if(self.ipAddress == None):
            raise Exception("Could not get system IP Address")
        if(self.folderToShare == None):
            raise Exception("path to folder to share is not setted")    


        # Instantiate a dummy authorizer for managing 'virtual' users
        authorizer = DummyAuthorizer()

        # Define a new user having full r/w permissions and a read-only
        # anonymous user
        authorizer.add_user(self.userNameFTP, self.userPasswordFTP, self.folderToShare , perm='elradfmwMT')
        
        if(self.FTPanomusAccess):
            authorizer.add_anonymous(homedir=self.folderToShare)

        # Instantiate FTP handler class
        handler = FTPHandler
        handler.authorizer = authorizer

        config_logging(level=logging.INFO)

        # Define a customized banner (string returned when client connects)
        handler.banner = "pyftpdlib based ftpd ready."
        address = (self.ipAddress, self.port)  # listen on every IP on my machine on port 21
        server = servers.FTPServer(address, handler)
        server.serve_forever()
 
    
    # function to operate the class methods
    # this function yields some messages and at last when is yields None then the server is started
    """ parameters = 
    folderToShare = path to folder to share via server
    port = port number to be used to start server
    http if true , http server will be started instead of ftp
    userOtherPort if True , if port passed is busy then some other port will be used and it will raise error
    logToConsole if false then no logging messages will be logged to console and server will be started as child process
    userNameFTP = userName for access to files in ftp server
    userPasswordFTP = password for userName to access files via FTP
    FTPanomusAccess = True , then read only ftp server will be opened which does not require user name and password to be connected """
    
    def start_fileShare(self , folderToShare , port = 8000 , http = False , useOtherPort = True , logToConsole = False , userNameFTP = "user" , userPasswordFTP = "225588" , FTPanomusAccess = True):
        
        # setting things up
        self.setSharePath(folderToShare)
        self.ipAddress = self.get_ip_address()
        self.http = http
        self.setPort(port , useOtherPort)


        self.userNameFTP = userNameFTP
        self.userPasswordFTP = userPasswordFTP
        self.FTPanomusAccess  = FTPanomusAccess

        self.logToConsole = logToConsole

        # if we need to start http server
        if(self.http):
            yield "Visit http://{}:{} in browse to download files".format(self.ipAddress , self.port)
            yield "Files only available to devices connected to the same network"

            if(self.logToConsole):
                yield "press ctrl c to stop server"
                yield None

                self.startServerAtFolderSettedHTTP_log()
            
            else:
                yield None
                self.mulProcess1.start()


        # else ftp server will be started
        else:
            if(self.FTPanomusAccess):
                yield "Visit ftp://{}:{} in file explorer or FTP browse to download files".format(self.ipAddress , self.port)
                yield "For Uploading as well Visit ftp://{}:{}@{}:{} in same".format(self.userNameFTP , self.userPasswordFTP , self.ipAddress , self.port)
            else:
                yield "Visit ftp://{}:{}@{}:{} in file explorer or FTP browse".format(self.userNameFTP , self.userPasswordFTP , self.ipAddress , self.port)
            
            
            yield "Files only available to devices connected to the same network"
            
            if(self.logToConsole):
                yield "press ctrl c to stop server"
                yield None
                self.startServerAtFolderSettedFTP_log()


            else:
                yield None
                self.mulProcess2.start()

        return


    # method to stop file share
    def stopFileShare(self):
        try:
            if(self.http):
                self.mulProcess1.terminate()
            else:
                self.mulProcess2.terminate()
            
            # resetting the modules
            modulenames = set(sys.modules) & set(globals())
            allmodules = [sys.modules[name] for name in modulenames]
            for i in allmodules:
                reload(i)

            self.__init__()

        except AttributeError:
            modulenames = set(sys.modules) & set(globals())
            allmodules = [sys.modules[name] for name in modulenames]
            for i in allmodules:
                reload(i)

            self.__init__()
            raise RuntimeError("file share is already stopped")

       

        

# for testing purpose
if __name__ == "__main__":
    pass
    # fil = FileShareClass()
    # for i in (fil.start_fileShare("/home/harshnative" , http = True , logToConsole=True , port=5001 , useOtherPort=True)):
    #     print(i)

    # import time
    # # time.sleep(60)
    # fil.stopFileShare()