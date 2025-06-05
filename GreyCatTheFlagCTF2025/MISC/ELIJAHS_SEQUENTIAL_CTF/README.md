## Elijah's Sequential CTF
### **Problem Summary:**

Elijah is given a sequence of problems, each from one of 3 categories:

* 0: Reverse Engineering
* 1: Binary Exploitation
* 2: Cryptography

He can choose any **subsequence** of problems to solve. His **satisfaction score (`s`)** increases based on *pairs* of **consecutive solved problems** from different categories, as follows:

| Previous → Current | Satisfaction Increase |
| ------------------ | --------------------- |
| 0 → 1              | 2                     |
| 1 → 2              | 5                     |
| 0 → 2              | 3                     |
| 1 → 0              | 4                     |
| 2 → 0              | 1                     |
| 2 → 1              | 6                     |

Goal: **Select a subsequence to maximize `s`**.

---

### **Solution Approach (Dynamic Programming):**

The idea is to track the **maximum satisfaction** that ends with solving a challenge of a specific category.

#### Variables:

* `dp0`: Max satisfaction if the last chosen problem is category 0
* `dp1`: Max satisfaction if the last chosen problem is category 1
* `dp2`: Max satisfaction if the last chosen problem is category 2


#### For each challenge:

Depending on the current challenge's category (`x`):

* Update `dpX` by checking all possible transitions from previous `dpY` values (if defined), adding the appropriate satisfaction value.

#### Example Transitions:

If the current problem is `0`:

* From previous `0`: just carry forward value.
* From `1`: add 4 (1 → 0)
* From `2`: add 1 (2 → 0)

Repeat similarly for `1` and `2`, using the satisfaction rules.

---

### **Result**

At the end, the result is:

```c
max(dp0, dp1, dp2)
```

