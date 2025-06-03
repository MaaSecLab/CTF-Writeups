# GreyCat CTF 2025 – Layer Cake (973 pts)

Challenge Description
---------------------
Layer cake is so good. I have an mp3 file all about layer cake. Maybe you can find the flag there?

We're given a suspicious 'layer cake.mp3' file and told to “find the flag there.” The title and description strongly hint that this file has multiple layers, possibly steganography or file-format abuse.

Step 1: Check the File Type
---------------------------
The MP3 file wouldn’t play. I checked its real nature with binwalk, a tool for finding embedded files:

    binwalk -e "layer cake.mp3"

This revealed several embedded ZIP entries, including files like:

    layers/word/document.xml,
    layers/word/styles.xml,
    layers/[Content_Types].xml,


This structure matched that of a Microsoft Word (.docx) file in disguise.

Step 2: Deal with the Embedded Zip
----------------------------------
Binwalk extracted a file named 45.zip. Trying to unzip it the normal way failed:

    unzip 45.zip
    # error: missing 69 bytes... overlapped components

So we used bsdtar, which is more forgiving with broken zips:

    bsdtar -xf 45.zip

Now I had the full word/ directory structure typical of .docx files.

Step 3: Search for the Flag
---------------------------
I tried looking in the usual document.xml, but it was empty.

So I recursively searched all files for the grey{} flag pattern:

    grep -r -oEi "grey{{[^}}]+}}" .

And found it in styles.xml:

    grey{s0_f3w_lay3r5_w00p5}

Final Flag
----------
grey{s0_f3w_lay3r5_w00p5}
