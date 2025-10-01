## BIGMAK

### Problem Description

I tried typing out the flag for you, but our Astronaut Coleson seems to have changed the terminal's keyboard layout? He went out to get a big mak so I guess we're screwed. Whatever, here's the flag, if you can somehow get it back to normal.

rlk{blpdfp_iajylg_iyi}

### Solution

We know that we will have to work with keyboard layouts, so we will have to solve this challenge by reversing the mapping of one layout to the other. We can assume that the input would be formatted with the QWERTY layout, since that is the most widely used layout globally. We have to find the layout trough which it was processed. The description of the challenge mentions the name "Coleson" and in the title we have "MAK". Colemak is the most likely candidate, and translating the inputs back to QWERTY will give us the flag. 

sun{burger_layout_lol}


Have a great day :)
github.com/johnnnathan

