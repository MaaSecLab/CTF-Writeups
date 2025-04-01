## Midi Melody
### Problem Description
Midi is where the magic happens
### Solution

The program that is given to us accepts a series of flags as arguments (-m, -j, -r) and creates a .midi file depending on their configuration. The flags are actually substitutes for ' - ' ,  ' . ' and '   ', which is hinted in the help menu, after flags and before the ':' symbols. 
![[midi_help.png]]

The code that handles the file creation all exists in the main function, and is relatively simple. Select notes are stored in the form of numbers in the main function and they are added to the file sequentially. No secret operations are performed and that means that the flag is encrypted in the audio file that comes along with the program. We can attempt to reverse the flag configuration by looking at the hex code of the audio file, we can then generate our own and then cross-reference them to see where the chain is correct. This process can be automated but I was able to generate the correct configuration quickly by hand.

![[comparisonn.png]]

![[morse_decoded.png]]



Have a great day :)
github.com/johnnnathan
