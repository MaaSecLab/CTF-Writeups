
## Challenge Description  
> *The party just ended, but people are hungry. Find the nearest fast food spot to see where everyone went!*  

### Flag Format  
- The flag follows this format: `swampCTF{...}`  

---

## Solution  

### 1. Using Coordinates from the Previous Challenge  
Since this challenge follows the **party house** challenge, we reused the **GPS coordinates** we had previously extracted:  
- **29° 39' 10.32" N, 82° 19' 59.68" W**  

---

### 2. Searching for Nearby Fast Food Restaurants  
We used **Google Maps** to search for **fast food places near the extracted location**.  

#### **Steps Taken:**  
1. Entered the **GPS coordinates** into Google Maps.  
2. Looked for **nearby fast food locations**.  
3. The closest listed fast food place was **Checkers**, but initially, we found nothing.  
4. Checked **other nearby restaurants**, but no clear hints emerged.  

---

### 3. A new approach  
Realizing that **flags can sometimes be hidden in unexpected places**, we brainstormed where additional clues could be stored.  

We considered:  
- **Business descriptions**  
- **User reviews**  

---

### 4. Finding the Flag  
We returned to **Checkers** and sorted the **Google Reviews by "Newest"**.  

A recent review contained the flag:  
```plaintext
swampCTF{Checkers_Yum}
```

---

## Tools Used  
- **Google Maps** – To locate fast food places near the GPS coordinates  
- **Google Reviews** – To check for hidden clues  


---

🏆 **Flag:** `swampCTF{Checkers_Yum}`
