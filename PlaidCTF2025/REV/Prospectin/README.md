## Fool's Gulch 
### Problem Description
Welcome to Fool's Gulch, prospector! Word around the saloon is that old Jeremiah Plaid struck gold somewhere in these hills before he disappeared. His journal entries mention a secret sequence that leads to The Mother Lode - the richest gold vein in all the territory. Can you decipher Jeremiah's cryptic notes and find the treasure that's eluded so many fortune seekers? Enter the correct sequence, and you might just strike it rich! Remember, not all gold that glitters is worth the same. The purer your find, the higher your claim will be valued at the assayer's office.

Old Man Jenkins' map to his modest gold claim has been floating around Fool's Gulch for years. Most think it's worthless, but you've noticed something peculiar in the worn-out corners...

https://plaidctf.com/files/prospectin.cdc5496a4fa3697a4e15149f7493ebfb7e576f674e9ebff8990fc2fa0129375b.tgz

### Solution
An ELF file is given and by looking at it with Ghidra it shows that points can be earned for every if statement that is true (there are 400 of them). Not all statements have to be true and upon further investigation you'll see that some are opposites of each other and can never both be true. I used Z3 with every character of the flag being a variable and all 400 constraints being soft constraints added to the solver. After running this for some sec the flag is returned in hex. Cyberchef is used to translate to UTF-8 and then the string is reversed. 

Have a nice day :D

https://github.com/mlwauben
