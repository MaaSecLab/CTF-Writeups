## Name
Lunar Auth
### Problem Description

Infiltrate the LunarAuth admin panel and gain access to the super secret FLAG artifact!

### Solution

On the index page, I didn't see anything interesting. So I checked the robots.txt which contained the link to the admin route.

I visited the /admin route and saw a login form. I tried to login with some random credentials but it didn't work and it showed a pop-up with an error message.

I looked into the page source code and found in the script tag that the login credentials were hardcoded with base64 encoding.

```
const real_username = atob("YWxpbXVoYW1tYWRzZWN1cmVk");
const real_passwd   = atob("UzNjdXI0X1BAJCR3MFJEIQ==");
```

I decoded the base64 strings to get the username and password with cyberchef and got:

```
username: alimuhammadsecured
password: S3cur4_P@$$w0RD!
```

Using these credentials, I was able to log in to the admin panel and get the flag.
Flag: `sun{cl1ent_s1d3_auth_1s_N3V3R_a_g00d_1d3A_983765367890393232}`