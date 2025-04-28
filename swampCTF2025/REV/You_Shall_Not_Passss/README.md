## You Shall Not Passss
### Problem Description
To enter in, you’ll need a key, A secret code just meant for thee. Type it right, don’t make a slip, Or you’ll be locked out—oops, that’s it!

### Solution

Open the executable using a disassembler and find the main function. Inside it some XOR operations are performed. These XORs do not operate upon the password but rather generate the "Correct!" and "Incorrect" strings to prevent finding them through looking for strings. Another function is called at the end of the main function, inside of which mmap is used to generate the function that handles the input, output and password validation. This means that we need to use a debugger, since the function is not able to be generated easily through only static analysis.  
![[decompiled_function.png]]
The characters in the given password are iterated over and passed through the operations that make up the body of the while loop. The encrypted character is then compared against the stored encrypted character and the loop and a negative value is given to the status of the program if any of the characters are not equal. At the end of the function the correct message is shown depending on the status code of the loop. 

We can brute-force the password by replicating the code and modifying a bit to allow for easier password testing. We sequentially test the printable at an index before moving onto the next one. We can then check how many characters were valid to detect correct characters. The code can be found in script.c.




Have a great day :)
github.com/johnnnathan
