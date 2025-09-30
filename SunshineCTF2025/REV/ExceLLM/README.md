## Name
ExceLLM

### Problem Description
Did you know that the Apollo Guidance Computer used to land on the moon only had clock frequency of 2.048 MHz and about 4kb of RAM? In a similar vein of resource constraints, did you know you can implement machine learning models using Excel if you try hard enough? Our flag checker model is trained specifically to recognize the correct flag. Give it a shot!

### Solution
## Overview

I was given an Excel spreadsheet (`ExceLLM.xlsx`) that supposedly
contained a machine learning model trained to recognize the correct
flag. The twist was that the model was entirely implemented using Excel
formulas and matrices of weights!

My task: reverse-engineer the sheet and extract the flag.

------------------------------------------------------------------------

## Step 1: Inspecting the Workbook

The Excel file had four sheets:

-   **LLM** -- an interface with an input box ("Enter flag:") and a
    result field showing ✅ Correct / ❌ Incorrect.
-   **BITS** -- formulas that converted each character of the input flag
    into bits (ASCII to binary).
-   **WEIGHTS** -- a big matrix of numbers, clearly neural network
    weights.
-   **VERIFY** -- lots of formulas combining BITS and WEIGHTS with
    SUMPRODUCT, MAX(0,...), etc. This looked exactly like layers of a
    neural net.

The `LLM` result cell depended on `VERIFY!Z1`, which in turn checked
whether the outputs of 27 sub-networks were all correct.

------------------------------------------------------------------------

## Step 2: Understanding the Network Structure

Each character of the flag was handled by its own little neural network:

-   Input: 8 bits (from `BITS`).
-   Hidden layer: 8 neurons with ReLU activation (`MAX(0, …)`).
-   Output: 1 neuron with a threshold (`> 0`).

Each block of weights (in the **WEIGHTS** sheet) corresponded to one
character position.

So the Excel sheet was literally running **27 small binary
classifiers**, one for each character in the flag.

------------------------------------------------------------------------

## Step 3: Reimplementing the Model in Python

Excel wasn't giving me the evaluated result since no flag was entered.
So I extracted the weights with Python (`openpyxl`) and reimplemented
the network:

``` python
import numpy as np

def run_block(char_code, W_in, b_h, w_out, b_out):
    bits = np.array([(char_code >> (7-i)) & 1 for i in range(8)])
    hidden = np.maximum(0, (bits @ W_in + b_h) / 100.0)
    out = (hidden @ w_out + b_out) / 100.0
    return out > 0
```

Then, for each of the 27 character positions, I brute-forced all
printable ASCII characters and kept only those that passed their
respective classifier.

------------------------------------------------------------------------

## Step 4: Recovering the Flag

When I ran the brute force, every position had exactly **one valid
character**:

    1: s
    2: u
    3: n
    4: {
    5: n
    6: 0
    7: t
    8: _
    9: q
    10: u
    11: 1
    12: t
    13: 3
    14: _
    15: c
    16: h
    17: 4
    18: t
    19: _
    20: G
    21: P
    22: T
    23: _
    24: l
    25: 0
    26: l
    27: }

Concatenating them gave the final flag:

    sun{n0t_qu1t3_ch4t_GPT_l0l}

------------------------------------------------------------------------

Flag: `sun{n0t_qu1t3_ch4t_GPT_l0l}`.
