## THE-MASTER 

### Problem Description
trust me bro, i know what im talking about. im the master when it comes to these things. what street are we on?

### Solution

For this challenge we are given a single street-view image of a random road in the state of Ohio. All meta-data has been scraped from the image, so we have to base our assumptions off of the contents of the image.  

On one of the boards on the far left side of the image, we can see the text "MORGAN" with the outline of the stae of Ohio in the background. The board also shows a yellow line overlayed on top of the state. Another board shows "TRAIL X-ING" which is only present in locations with walkable trails near them. A few KIMBLE bins can be found scattered by the street which is a Garbage Disposal company that is active in the county of Morgan. 

There was not much more usable information, and some possible leads were locked behind low picture quality. We looked for possible maps of KIMBLE bins online but there was no such thing. We then searched for the name of the path that the board was pointing to and realized that it was most likely the Buckeye Trail, which mapped perfectly onto the line on the "Morgan" board.

Using [this](https://www.buckeyetrail.org/overview.php) website we guessed that the most likely city candidates were Stockport and Chesterhill. We searched inside the bounds of the city, but were unsucessful in finding anything of note. 

After some dead-ends we looked at the image again, building our assumptions from the ground up. We focused a bit more on the architecture on display and reverse image searched the big red building near the center of the image. It immediately returned an exact result, that being the Lore City United Methodist Church. From there it was a simple google maps search and correct flag formatting.

Have a great day :)
github.com/johnnnathan
