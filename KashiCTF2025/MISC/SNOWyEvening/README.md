## SNOWy Evening
### Problem Description
A friend of mine , Aakash has gone missing and the only thing we found is this poem...Weirdly, he had a habit of keeping his name as the password.

We are given a text file "poemm.txt"

### Solution
When opening the file we can see that there is a weird whitespace padding structure added to the text, which makes us think there should be something hidden inside it. The answer is visible in the title of the challenge "SNOW" which is an encoding scheme (https://darkside.com.au/snow/). Using the software to decode the hidden message along with the password from the problem statement: ```snow -C -p Aakash poemm.txt``` we get https://pastebin.com/HVQfa14Z which has a text written with Moo's. The pastebin document is encoded using the MOO cipher, which, after decoding gives us the flag: ```KashiCTF{Love_Hurts_5734b5f}```

Have a great day!
[github.com/serbanescumihnea](https://github.com/serbanescumihnea)
 
