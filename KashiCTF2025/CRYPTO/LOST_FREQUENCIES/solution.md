## LOST FREQUENCIES 
### Problem Description

Zeroes, ones, dots and dashes
Data streams in bright flashes

111 0000 10 111 1000 00 10 01 010 1011 11 111 010 000 0

NOTE: Wrap the capitalized flag in KashiCTF{}

### Solution

The description of the challenge makes it quite apparent that we will have to use morse to find the flag. The encoded string they game us is in binary format, so we will have to transform it into valid morse. We can get the valid morse code by finding and replacing every instance of "1" with "-" and "0" with ".". Doing so will give us:

`
--- .... -. --- -... .. -. .- .-. -.-- -- --- .-. ... .
`

which if decoded using an online translator will give us the flag.


Have a great day :)
github.com/johnnnathan
