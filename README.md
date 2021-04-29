# Jarvis2.O
New and better console based personal assistant

</br>
</br>
</br>
</br>
</br>


# Website
https://www.letscodeofficial.com/jarvis


</br>
</br>
</br>
</br>
</br>

# Download
visit https://www.letscodeofficial.com/jarvis_downloads



</br>
</br>
</br>
</br>
</br>

# Updating 
You can update jarvis by either running this command inside jarvis

```
update jarvis
```

OR just downloading and installing the latest version


</br>
</br>
</br>
</br>
</br>


# Installing
</br>

## 1. Windows

visit - https://www.letscodeofficial.com/jarvis_downloadWindows2
</br>
</br>

## 2. Linux (Ubuntu/Debian)

visit - https://www.letscodeofficial.com/jarvis_downloadLinux2
</br>
</br>

You can run sudo jarvis command without password also
</br>

just run this command in jarvis and follow instructions
```
add me to root
```
</br>
or run this command in terminal -

```shell
sudo gedit /etc/sudoers
```

then add this line to end of file
```
username ALL = (root) NOPASSWD: /bin/jarvis
```

remember to replace the username with your user name , you can find your username by running this command in terminal - 

```shell
whoami
```

</br>
</br>
</br>
</br>
</br>


# Online Documentation

visit - https://www.letscodeofficial.com/jarvis_docs_home


</br>
</br>
</br>
</br>
</br>


# Improvement to previous Gen Jarvis
link to previous gen jarvis - https://github.com/harshnative/JARVIS

from development point of view - 

1. Designed with modularity in mind that is all the internal function and packages returnes data to main function instead of priting is write away making them reusable anywere

2. better error handling and logging system

3. better caching and optimising in internal function

4. easily scalable

5. many more features



</br>
</br>
</br>
</br>
</br>

# Features

Jarvis 2.O can do many things such as

1. weather of any city
1. speed test
1. own settings file
1. password manager with military class encryption
1. Share file via both HTTP and FTP server with both wired and wireless medium.
1. mispelled command detection
1. auto complete command using tab
1. in built troubleshooter


More comming soon (^_^)



</br>
</br>
</br>
</br>
</br>


# OS suppport
Jarvis is currently desinged , tested and maintained for linux and windows only.

But project itself is made in python as has many other supported platform, making some changes the code should be able to make jarvis run on any operating system.


</br>
</br>
</br>
</br>
</br>

# Documentation
<a href="#Weather">1. Weather</a>
</br>
<a href="#Speed-Test">2. Speed Test</a>
</br>
<a href="#Settings">3. Settings</a>
</br>
<a href="#File-Share">4. File Share</a>
</br>
<a href="#Password-Manager">5. Password Manager</a>
</br>
<a href="#Auto-Completion">6. Auto Completion</a>
</br>



</br>
</br>
</br>
</br>
</br>


<h2 id="Weather">
1. Weather
</h2>

```
weather cityName
```

Were cityName can be anything.
ex - london , new york


If no city name is passed then Jarvis check for the city name in city file

you can set the default city name in settings file.


</br>
</br>
</br>
</br>
</br>

<h2 id="Speed-Test">
2. Speed Test
</h2>

```
speed test
```

Will perform the speed test and average it 2 times by default to show you the most accurate real world result

</br>
</br>

```
speed test -b
```
If you want the result in mega bytes instead of mega bits

</br>
</br>

```
speed test 3
```
If you want the result to be averaged 3 times instead of 2

averaging is limited to max 5 times

</br>
</br>

```
speed test -b 3
```
You can combine the commands



</br>
</br>
</br>
</br>
</br>


<h2 id="Settings">
3. Settings
</h2>

```
open setting
```
To open the settings file

</br>
</br>

```
update setting
```
To apply the newly updates settings in Jarvis 


</br>
</br>

```
restore setting
```
To restore the settings file to default value 

</br>
</br>
Default settings file looks like - https://github.com/harshnative/Jarvis2.O/blob/main/defaultSettings.txt


</br>
</br>
</br>
</br>
</br>



<h2 id="File-Share">
4. File Share
</h2>

```
start file share
```
To start a ftp server
A window will be prompted to select the location to share

</br>
</br>
Options for start file share command - 

1. http
```
start file share http
```
To start a http server
usefull when you cannot access the ftp server
Remember you can only download files using http server
</br>

2. -d
```
start file share -d
```
To start a server at default folder grabed from the settings file
If you cannot access the ftp server
Remember you can only download files using http server

3. -log
```
start file share -log
```
when you want to see realtime status of server
</br>

4. -a
```
start file share -a
```
when you want to allow anonymous access to FTP server , that is without ID password
</br>

5. command can be clubbed together
```
start file share http -d -log
```

</br>
</br>


```
stop file share
```
To stop file share
</br>
</br>


```
set file share port PORTNUMBER
```
To set custom file share port if the default file share port is busy in your machine which is 5000

were PORTNUMBER can be from 1000 to 9999

when the port number assigned is busy , jarvis automatically chooses a free port
</br>
</br>


```
show file share
```
Show the output created by file share again to see the exact intructions to connect

</br>
</br>
</br>
</br>
</br>



<h2 id="Password-Manager">
5. Password Manager
</h2>

```
password
```
To start password manager

</br>

For the first time you will need to set the password for encryption.

password should be strong enough containing mixture of characters and min 8 chars in length.

You can also set a custom path to database in settings file (path should also contain the name of db like /user/mypasswords.db)

</br>

```
-a
```
To add a password
</br>
</br>


```
-a -m 
```
To add a multi line password

You will need to press on a new line - ctrl + d on linux or ctrl + z on windows to stop entering and add it
</br>
</br>

```
-u
```
To update a password
</br>
</br>




```
-d
```
To delete a password
</br>
</br>



```
-s
```
To see a password
</br>
</br>



```
-sa
```
To see all password 
</br>
</br>


```
-c
```
To change password 
</br>
</br>



```
-sa all
```
Jarvis has started to crush the long references and passwords while showing them in -sa to maintian a cleaner look

To see all the characters in reference and passwords you can add all to the command

like 
-sa all
-u all 
-d all

</br>
</br>
</br>
</br>
</br>

<h2 id="Auto-Completion">
6. Auto-Completion
</h2>

After writing some part of the command you can press tab to auto complete it

Auto completion does not work when entering variables.




</br>
</br>
</br>
</br>
</br>



# Some backend details

1. Storage directory : On windows jarvis stores user file such as logs , settings , data bases etc in C:\programData\JarvisData. While in ubuntu it stores in /opt/JarvisData.

2. Encryption used in password Data base - Jarvis uses military class encryption technique provided by easySED module to securely store your passwords. you learn more about easySED at https://www.letscodeofficial.com/pySEDDocs



</br>
</br>
</br>
</br>
</br>


# Contributors
<a href="https://www.letscodeofficial.com/"><img src="https://www.letscodeofficial.com/static/images/favicon.ico" width="150" height="150" /><h3>Lets Code Official</h3></a>


</br>
</br>
</br>

<a href="https://github.com/harshnative/"><img src="https://www.letscodeofficial.com/static/images/jarvis/HarshNativeProfile.JPG" width="150" height="150" /><h3>Harsh Native</h3></a>


More contributors are listed on website - https://www.letscodeofficial.com/jarvis_contributors



</br>
</br>
</br>
</br>
</br>


# Donate 🥰
You can donate at https://www.letscodeofficial.com/jarvis_contribute


</br>
</br>
</br>
</br>
</br>


# Contribute
Comming soon 



</br>
</br>
</br>
</br>
</br>


# license
Jarvis is licensed under GNU GENERAL PUBLIC LICENSE VERSION 3

Visit www.letscodeofficial.com/gnuV3 for license terms

