## Beginner Web

### Description

Hey, my son Timmy made his first website. He said he hid a 'secret' message within different parts of the website... can you find them all? I wanna make sure he isn't saying any swear words online.

The flag is broken up into 3 parts. The parts of the flag should be concatenated in the order they are numbered and then surrounded by the standard wrapper. For example: 'swampCTF{' + part1 + part2 + part3 + '}'

### Solution

The first part of the flag could be found directly in the HTML code. It was in a comment at the top of the code.
```html
<!--Part 1 of the flag: w3b_"-->
```

Looking further in the html code we see two Javascript files.
```html
<script src="polyfills-FFHMD2TL.js" type="module"></script>
<script src="main-34VY7I6V.js" type="module"></script>
```

Inside the first file I did not find anything.

The second file contained a string with "flag" in it.
```javascript
this.cookieService = t;
let n = "flagPart2_3"
    , r = "U2FsdGVkX1/oCOrv2BF34XQbx7f34cYJ8aA71tr8cl8="
    , o = "U2FsdGVkX197aFEtB5VUIBcswkWs4GiFPal6425rsTU=";
this.cookieService.set("flagPart2", $n.AES.decrypt(r, n).toString($n.enc.Utf8), {
    expires: 7,
    path: "/",
    secure: !0,
    sameSite: "Strict"
});
let i = new Headers;
i.set("flagPart3", $n.AES.decrypt(o, n).toString($n.enc.Utf8)),
fetch("/favicon.ico", {
    headers: i
})
```

The string "flagPart2_3" is the key used to decrypt the two other parts of the flag. The first part is stored in a cookie and the second part is sent in the headers of a request to "/favicon.ico".

Finding the third part was easy. I opended the networ tab in the dev tools and looked at the requests headers of the request to "/favicon.ico". The third part was in the headers.
```javascript
flagpart3: c0mpl1c473d
```

The second part was stored in the cookies. I tried to inspect the cookies in the http requests but I could find any because secure !0 set the cookie to HTTPS only, but the site was using http.

So I decrypted the cookie "U2FsdGVkX1/oCOrv2BF34XQbx7f34cYJ8aA71tr8cl8=" using the key "flagPart2_3" and got the second part of the flag.
```javascript
const CryptoJS = require('crypto-js');
const key = "flagPart2_3";
const flagPart2 = "U2FsdGVkX1/oCOrv2BF34XQbx7f34cYJ8aA71tr8cl8=";
const decrypted2 = CryptoJS.AES.decrypt(flagPart2, key).toString(CryptoJS.enc.Utf8);
console.log("flagPart2:", decrypted2);
```

The output was: flagPart2: br0w53r5_4r3_

The final flag is:
```
swampCTF{w3b_br0w53r5_4r3_c0mpl1c473d}
```