
# CTF Write-up: GPS Metadata Extraction  

## Challenge Description  
> *This party house is known for its 3AM outings, but you've gotta work for the location if you want to come! Enter the GPS coordinates of the location!*  

### Flag Format  
The flag follows this format:  
- `swampCTF{xx.xx.xx,xx.xx.xx}`  
- `swampCTF{xx.xx, xx.xx}`  

### Provided File  
- `IMG_4048.HEIC`  

---

## Solution  

### 1. Understanding the File Format  
The provided image is in **HEIC format**, which is commonly used by iPhones. Unlike PNG or JPG, HEIC retains extensive metadata, including **GPS coordinates** if location services were enabled when the photo was taken.  

---

### 2. Extracting Metadata  
Since we were looking for **GPS coordinates**, we used `exiftool`, a powerful metadata extraction tool.  

#### **Command Used:**  
```bash
exiftool -GPS* IMG_4048.HEIC
```
  
This command specifically extracts **GPS-related metadata** from the image.  

#### **Extracted Data:**  
```
GPS Position                    : 29 deg 39' 10.32" N, 82 deg 19' 59.68" W
```

---

### 3. Formatting the Flag  
According to the challenge instructions, we formatted the coordinates into the required flag format:  

```plaintext
swampCTF{29.39.10,82.19.59}
```

---

## Tools Used  
- **`exiftool`** – Extracting metadata from the HEIC image  
- **HEIC File Analysis** – Understanding metadata storage in HEIC files  
- **Text Processing** – Formatting the extracted GPS coordinates  

 

---

🏆 **Flag:** `swampCTF{29.39.10,82.19.59}`  
