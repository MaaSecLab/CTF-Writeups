## t0le t0le 
### Problem Description
Our CCDC business guy made a really weird inject. He's just obsessed with that damn cat... there's nothing hiding in there, right?

A docx file titled **Team_5_-_Inject_72725.docx** was also provided


### Solution

install oletools in a python environment.

```
pip install toletools
```

then run `oleobj` on the file. This tool is used to extract embedded objects from OLE files.

```
oleobj Team_5_-_Inject_72725.docx
```


a temp file will be generated called **Team_5_-_Inject_72725.docx_vro**


open it and copy its contents into cyberchef. In the recipe, put `from Base64` and then run `ROT13 Brute Force`. Then, you will get the flag 

### Result

```
sun{t0le_t0le_my_b3l0v3d!}
```

Have a great day :D [https://github.com/JoelDha](https://github.com/JoelDha)
