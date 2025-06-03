## Secret Development Kit 

### Problem Description
You have just stolen top secret production files of a secret board. Hmm, I wonder what it could be?

### Solution

We are given a .zip file containing a lot of .gbr files. This file format is used for visualization of PCB boards on digital systems. Using a tool like [pcbway](https://www.pcbway.com/project/OnlineGerberViewer.html) will allow us to handle the files more easily. The bottom silkscreen component contains the flipped string "grey{see_grey?????/????_?_??????_??}" with "section_1", "section_2", "event?" and "secret_pin_no" pointing to their respective fractions, in the bottom left. 

In the same layer we can find "m3ch4rp??5?". On the soldermask layer we can find "4rMy", and on the soldermask layer in the top section we can find "@_f1n4l5".

Putting it all together we get "grey{see_greym3ch4/4rMy_@_f1n4l5_??}". The secret_pin_no value is missing, but we managed to find it, by luckily guessing that it was 25. Landing on 25 otherwise, would require us to look at the board configuration, and finding the pin that is connected to the solder point, which is GPIO25 (Credit to user "Leo" on the gctf discord server).

Finally we get "grey{see_greym3ch4/4rMy_@_f1n4l5_25}"
