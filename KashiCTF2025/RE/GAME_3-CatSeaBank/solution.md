## CATSEABANK 
### Problem Description
We made a game.

https://drive.google.com/file/d/1R5EdsswQydsUQZIToQDkR-1CpwRIzmiK/view?usp=drive_link


### Solution
Yet another game challenge. Running the game we are set on a 2D map with a Bank building on the left side and a man, the "Hinter", on the right side. Although the player starts with no money, we are able to withdraw 1000 coins from the bank. The "Hinter" says to us that we need to "Pay 2000" to "succeed". Since there is nothing else to do, we can try to somehow reach the 2000 coin mark with only the 1000 at our disposal. There are two ways to generate enough money. The first one is to open CheatEngine and connect it to the process. Then keep scanning for the amount of money we have currently while depositing and withdrawing money from the bank. Once we locate the location of the money, we can modify the value and give ourselves an arbitrary amount of money and pay the 2000 required. The second is to recover the scripts of the game with a tool such as ILSpy or dotNet and the find the script where the bank transactions are handled. We can see that the bank's code is not entirely secure and allows us to withdraw negative amounts of money. If we do that enough times we can overflow the value and receive a positive amount of money. Once we pay the "Hinter" the money a button appears with the label "Get Wisdom" if we click on it nothing happens. Looking again at the decompiled scripts we can see that the button itself has no code assigned to it. That means that clicking it does literally nothing. 

There exist some tools that allow us to extract assets from a Unity Project. Loading up the project into AssetStudio will list all of the assets that are stored in it. If we filter by type or size we find a two audio files, one called "wise.wav" and another "flagfile.wav". The "wise.wav" file contains a cryptic message regarding artifacts spoken by a wise old man, and "flagfile.wav" what seems like static sound. If we load "flagfile.wav" into SonicVisualizer to retrieve the spectogram image of the noise, we will find the challenge's flag in image form.


Have a great day :)
github.com/johnnnathan
