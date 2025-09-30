## Pretty Delicious Food

### Problem Description
This cake is out of this world! :DDDDDDD

omnomonmonmonmonm

...

something else is out of place too.

Note: This is not a steganography challenge

### Solution
The PDF hides a Base64 string in an inline JavaScript snippet. Decoding it gives the flag:

sun{p33p_d1s_fl@g_y0!}


---

My Process
1) Reading the prompt
The note in the challenge said “This is not a steganography challenge.” That made me skip any stego/image tricks and focus on the PDF’s text layer and embedded code.

2) Inspecting the PDF
I opened the PDF and searched through the text. Running strings or pdfgrep quickly revealed a suspicious JavaScript snippet:

const data = 'c3Vue3AzM3BfZDFzX2ZsQGdfeTAhfQ==';


3) Recognizing Base64
That string looked exactly like Base64. No obfuscation, just plain encoding.

4) Decoding the string
I decoded it with a simple one-liner:

echo 'c3Vue3AzM3BfZDFzX2ZsQGdfeTAhfQ==' | base64 -d


or in Python:

python3 -c "import base64;print(base64.b64decode('c3Vue3AzM3BfZDFzX2ZsQGdfeTAhfQ==').decode())"


It printed:

sun{p33p_d1s_fl@g_y0!}


5) Wrapping up
That was clearly the flag, and it matched the format perfectly. No further layers needed.

---

Final Flag
sun{p33p_d1s_fl@g_y0!}
