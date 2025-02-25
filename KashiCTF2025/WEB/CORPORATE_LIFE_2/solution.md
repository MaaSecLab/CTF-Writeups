## Corporate Life 2
### Problem Description
The disgruntled employee also stashed some company secrets deep within the database, can you find them out?

### Solution
The "Corporate Life 2" follows the "Corporate Life 1" solution. This challenge focuses on SQL Injection vulnerability. By analyzing network traffic with Burp Suite, we identify a GET request for the build manifest. This request reveals the presence of the /v2-testing page, which we can access.(nothing new, this follows "COrporate Life 1" solution). 

Once inside /v2-testing, the next step is to enumerate the database structure. To do this, we must first determine the database type. Using SQLMap, we discover that the backend is running SQLite.

To explore the database schema, I used:

```bash
{"filter": "doesnotexist' union SELECT sql, null, null, null, null, null FROM sqlite_schema --"}
```

It reveals that database contains `flags` table. To retrieve the flag, I used this SQL query:

```bash
{"filter": "doesnotexist' union select null, secret_flag, null, null, null, null from flags --"}
```

Upon executing this query, we successfully retrieve the flag!
