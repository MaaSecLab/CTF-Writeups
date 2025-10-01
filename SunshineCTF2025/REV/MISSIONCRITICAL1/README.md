## Missioncritical1

### Problem Description

Ground Control to Space Cadet!

We've intercepted a satellite control program but can't crack the authentication sequence. The satellite is in an optimal transmission window and ready to accept commands. Your mission: Reverse engineer the binary and find the secret command to gain access to the satellite systems.

### Solution

Decompile the main function and find that there is a "sun{%s_%s_%s} string with a few others following it. Replace the %s with the strings following it in order and submit it to get the success message.

The strings are "e4sy", "s4t3ll1t3" and "3131". Putting all together we have:

sun{e4sy_s4t3ll1t3_3131}

Have a great day :)
github.com/johnnnathan
