## Protect the Environment 

### Problem Description
Protect the earth? We can't even protect our environment variables...

### Solution

The author of the challenge gives us three files, libc version 2.27, the c code and the executable file. Inside the source code we can find a simple main function that reads a 64 byte string that holds the name of the operation the user wants to perform and another 64 bytes that with the name of the environment variable on which the user wants to perform the operation. 

The source code has implemented the 2 operations, the "protect" and "print" operations. The "print" operation prints the value of the variable to the terminal and the "protect" operation performs a single rot13 rotation on the Value assigned to the key. Since the entire implementation is very secure, we must find a way to print the value of the "FLAG" variable, despite it being disallowed by the program. 

The "getenv()" function works by looking at the memory where the environment variables are stored, and returns the VALUE of the KEY that matches with the name that is passed to it. By tricking the program into printing the value of FLAG, by using a different alias, we would be able to get the flag. Since we know how the flags are formatted "FortID{...}" we would also know the first 7 characters of the Value of the FLAG variable, and their subsequent rotated versions. The 'F' character is 19 rotations away from '='. With some local testing, I found out that using "print x" with the value of FLAG looking similar to "FLAG=x=..." wouldn't work, but calling "print FLAG=x" would. We can make this approach even more powerful by immediately replacing the 'x' with a '='. As a result we would have "FLAG==...", with "print FLAG" and "print FLAG=" pointing to the same area in memory (without the first character, which is replaced by '=') while using different aliases. We can rotate (protect) the VALUE of FLAG 19 times, to turn the 'F' from "FortID{...}" into a '='. Then we can use "print FLAG=" to get the rotated flag (with the '=' added to the front), and putting that through a reverse rot13 algorithm, we get the flag.


Have a great day :)
github.com/johnnnathan
