## OK BOOMER

### Problem Description

7778866{844444777_7446666633_444777_26622244433668}

alternatively (if that one is producing invalid results)

77778866{8444447777_7446666633_4447777_26622244433668}

### Solution

The combination of the cryptographic nature of the challenge and the title immediately made us think of old technology or old encoding techniques. We tried summing the blocks of the same digits and then mapping them onto alphabetic characters, but that didn't work. 

One of the ideas we had that it's somehow related to rotary phones and we quickly realized that it's a mapping function from phones with buttons, also known as the T9 cipher. Putting the text through a decoder will grant us the flag.


sun{the_phone_is_ancient}
