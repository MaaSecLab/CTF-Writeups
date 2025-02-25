## Restaurant
### Problem Description
I just asked for my favourite pasta and they gave me this. Are these guys STUPID? Maybe in the end they may give me something real. (Wrap the text in KashiCTF{})

**Imports:** pasta.jpg

### Solution
Once you have downloaded the image, go and analyze it using 
```
xxd pasta.jpg
```

The description hints at *"the end they may give me something real"* meaning we need to inspect the end of the file. At the end of the file, you will see something like this:
```bash
...
0000b740: 2323 2322 28b2 378c 6a32 228b 2323 2322  ###"(.7.j2".###"
0000b750: 28bf ffd9 baab aaab bbaa baab abba baba  (...............
0000b760: aaab aaba aaaa abaa baaa aaab aaaa aaaa  ................
0000b770: baba abab aaba baab abab abba aaab aabb  ................
0000b780: abab baba baab abaa aabb aaaa bba0       ..............
```

The JPG file ends with `ffd9`, and we notice a sequence of 'a' and 'b'. The flag is encoded using the **Bacon cipher** (and we have a `pasta.jpg` file, you get it??:D)

Once we decode it, the flag reveals itself: `THEYWEREREALLLLYCOOKING`