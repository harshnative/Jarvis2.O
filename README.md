# Jarvis2.O
New and better console based personal assistant

</br>
</br>
</br>
</br>


# Website
https://www.letscodeofficial.com/jarvis

</br>
</br>
</br>

# Download
visit https://www.letscodeofficial.com/jarvis_downloads


</br>
</br>
</br>

# Improvement to previous Gen Jarvis
link to previous gen jarvis - https://github.com/harshnative/JARVIS

1. Designed with modularity in mind that is all the internal function and packages returnes data to main function instead of priting is write away making them reusable anywere

2. better error handling and logging system

3. better caching and optimising in internal function

4. easily scalable


</br>
</br>
</br>
</br>

# Features

Jarvis 2.O can do many things such as

1. weather of any city
2. speed test
3. own settings file


More comming soon (^_^)


</br>
</br>
</br>
</br>

# Documentation

### 1. Weather

```
weather cityName
```

Were cityName can be anything.
ex - london , new york


If no city name is passed then Jarvis check for the city name in city file

you can set the default city name in settings file.

</br>
</br>

### 2. Speed Test
```
speed test
```

Will perform the speed test and average it 2 times by default to show you the most accurate real world result

</br>

```
speed test -b
```
If you want the result in mega bytes instead of mega bits

</br>

```
speed test 3
```
If you want the result to be averaged 3 times instead of 2

averaging is limited to max 5 times

</br>

```
speed test -b 3
```
You can combine the commands


</br>
</br>

### 3. Settings
```
open setting
```
To open the settings file

</br>

```
update setting
```
To apply the newly updates settings in Jarvis 


</br>

```
restore setting
```
To restore the settings file to default value 

</br>
Default settings file looks like - https://github.com/harshnative/Jarvis2.O/blob/main/defaultSettings.txt

</br>
</br>


### 4. File Share
```
start file share
```
To start a ftp server
A window will be prompted to select the location to share

</br>

```
start file share http
```
To start a http server
If you cannot access the ftp server
Remember you can only download files using http server
</br>


```
stop file share
```
To stop file share
</br>


```
set file share port PORTNUMBER
```
To set custom file share port if the default file share port is busy in your machine which is 5000

were PORTNUMBER can be from 1000 to 9999
</br>


```
show file share
```
Show the output created by file share again to see the exact intructions to connect
</br>
</br>



### 5. Password Manager
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



```
-u
```
To update a password
</br>




```
-d
```
To delete a password
</br>



```
-s
```
To see a password
</br>



```
-sa
```
To see all password 
</br>


```
-c
```
To change password 
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


# Some backend details

1. Storage directory : On windows jarvis stores user file such as logs , settings , data bases etc in C:\programData\JarvisData. While in ubuntu it stores in /opt/JarvisData.

2. Encryption used in password Data base - Jarvis uses military class encryption technique provided by easySED module to securely store your passwords. you learn more about easySED at https://www.letscodeofficial.com/pySEDDocs


# license
Jarvis is licensed under GNU GENERAL PUBLIC LICENSE VERSION 3

Visit www.letscodeofficial.com/gnuV3 for license terms

