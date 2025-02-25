## FINALGAME? 
### Problem Description
We searched his room and found chess pieces thrown here and there ..thankfully someone recorded the entire game

https://lichess.org/incUSy5k


### Solution

The lichess webpage gives us not much information about how the flag will be found. At first I thought that there would be cheat moves that we would have to detect, but they all seemed legal. The lichess website allows us to export games in a PGN format. This format contains all the information needed to replay a game. There exists an algorithm that is able to encode text into PGN file and decode PGN files into text. Using [Chess-Steganography][https://incoherency.co.uk/chess-steg/] we can easily find the flag of the challenge.


Have a great day :)
github.com/johnnnathan
