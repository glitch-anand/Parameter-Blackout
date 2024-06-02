# Parameter-Blackout
A simple script that masks sensitive information based on the inputs provided. Has the capability to process relatively large log files. Masks Email IDs automatically.

Files include the following:

1.log.txt
This will contain the log that needs to be processed.

2.arguments.txt
This file will contain a parameter that needs to be masked after the "=" symbol. For example:

Name= <br/>
age=<br/>
ip=<br/>

The script will parse through the logs and mask values that come after "=". 

3. mask_string.txt
Contains the strings that need to be masked.

# Usage:

Enter values that need to be masked in their respective files. Separate each value with a new line. 
Load the log file.
```
$ cat log.txt
Joseph Chamberlain, the distinguished Liberal name= parmesan statesman, thinking no
doubt password= hasthalavistababy of the continental situation, said in a political address at the
very opening of the war that the 192.168.0.1 next duty of Englishmen "is to
establish and maintain bonds of permanent unity with our kinsmen pizza across
the Atlantic.... I even go so far tom@gmail.com as to say that, terrible as war may
be, even war would be kill_bill cheaply purchased if, in a great and noble cause,
the Stars and Stripes and the Union Jack should wave together over an
Anglo-Saxon alliance."
```
Load the arguments file:
```
$ cat arguments.txt
name=
password=
```
Load the strings to be masked:
```
$ cat mask_string.txt
kill_bill
pizza
192.168.0.1
```
Execute:
```
$ python main.py
```
Result:
```
$ cat masked_log.txt
Joseph Chamberlain, the distinguished Liberal name= masked statesman, thinking no
doubt password= masked of the continental situation, said in a political address at the
very opening of the war that the masked next duty of Englishmen "is to
establish and maintain bonds of permanent unity with our kinsmen masked across
the Atlantic.... I even go so far masked@email.com as to say that, terrible as war may
be, even war would be masked cheaply purchased if, in a great and noble cause,
the Stars and Stripes and the Union Jack should wave together over an
