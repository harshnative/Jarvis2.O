# Jarvis2.O
New and better console based personal assistant

</br>
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

### 2. speed test
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

# settings
```
setting
```
To open the settings file

</br>

```
update
```
To apply the newly updates settings in Jarvis 


</br>
Default settings file looks like - https://github.com/harshnative/Jarvis2.O/blob/main/defaultSettings.txt

