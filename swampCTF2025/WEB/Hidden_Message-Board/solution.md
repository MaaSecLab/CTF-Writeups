## Hidden Message-Board

### Description

Somewhere on this message-board is a hidden flag. Nothing has worked so far but we have noticed a weird comment in the HTML. Maybe it's a clue?

### Solution

In the HTML code there was an div with an attribute "code".
```html
<div id = "flagstuff" code = ""></div>
```

There also was a function checkCode() which was called on each render of the page. It checked if the code attrivute of the div was equal to the string "G1v3M3Th3Fl@g!!!!"

```javascript
async function checkCode(){
    if(printFlagSetup != undefined){
        console.log(printFlagSetup.getAttribute("code"))

        if(printFlagSetup.getAttribute("code") === "G1v3M3Th3Fl@g!!!!"){
        const flag = await getFlag();
        setFlagValue("[flag]: " + flag);
        }
    }
}
```

The code attribute was empty, so we could just set it to the string and get the flag.

```javascript
document.querySelector("#flagstuff").setAttribute("code", "G1v3M3Th3Fl@g!!!!")
```

On the next render of the page, the checkCode() function was called and the flag was printed to the console.

### Flag

```
swampCTF{Cr0ss_S1t3_Scr1pt1ng_0r_XSS_c4n_ch4ng3_w3bs1t3s}
```

