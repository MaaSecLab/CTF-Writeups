Challenge Writeup: PCAP Flag Forensics
======================================

Challenge Description
---------------------
We were provided with a chall.pcap file and tasked with extracting a hidden flag embedded within the packet capture. The challenge hinted at analyzing traffic, likely HTTP-based, and reconstructing fragmented data.

Tools Used
----------

    Wireshark (for initial manual inspection),
    pyshark (Python wrapper for TShark),
    Python + base64 + re (regex for decoding fragments),
    TShark CLI (tshark.exe path explicitly set),


Investigation Strategy
----------------------

    Initial Inspection:
    Opening the .pcap in Wireshark revealed HTTP traffic with base64-looking data. These looked like fragmented messages possibly forming a flag.,


    Scripted Extraction:
    I built a Python script using pyshark to extract all payloads, search for base64 strings, decode them, and collect only those containing flag-relevant patterns.,


   Example logic:
   

   base64_regex = re.compile(r'\b[a-zA-Z0-9+/=]{8,24}\b')
   



    Fragment Detection:
    The script revealed multiple repeatable fragments like:
        grey{d,
        1d_1_j,
        us7_ge,
        7_p01s,
        on3d},
    ,


   These appeared repeatedly across different packets.

Reconstruction Logic
--------------------
The script grouped decoded fragments and attempted permutations for reconstruction. Using logic and some filtering (prefix + suffix matching), O arrived at:

   grey{d1d_1_jus7_ge7_p01son3d}

Final Flag
----------
grey{d1d_1_jus7_ge7_p01son3d}
