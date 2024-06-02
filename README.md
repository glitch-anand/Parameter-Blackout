# Parameter-Blackout
Simple script that masks sensitive information based on the inputs provided.


Files include the following:

1.log.txt
This will contain the log that needs to be processed.

2.arguments.txt
This file will contain parameter that needs to be masked after the "=" symbol. For example:

Name= <br/>
age=<br/>
ip=<br/>

The script will parse through the logs and mask values that comes after "=". 

3. mask_string.txt
Contains the strings that needs to be masked.

# Usage:

Enter values that needs to be masked in their respective files. Separate each value with a new line. 

Execute:
```
python main.py
```
