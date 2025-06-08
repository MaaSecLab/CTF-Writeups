# Shaker CTF Challenge Write-Up

This document explains formally how to solve the **Shaker** crypto challenge from GreyHats CTF. The challenge exposes an oracle that protects a 64-byte secret flag by repeating these operations:

1. **XOR-mask**: \(S \leftarrow S \oplus x\), where \(x\in\{0,1\}^{512}\) is a fixed 64-byte key.  
2. **Permute**: \(S \leftarrow \mathrm{perm}_p(S)\), for a secret random permutation \(p\) on 64 positions.  
3. **Leak**: Return \(S\), then internally reverse the mask and draw a new permutation.

A user action “See inside” performs

\[
S_{\mathrm{leak}} \;=\; (S_{\mathrm{old}} \oplus x)\quad\text{returned},
\]
\[
S_{\mathrm{old}} \leftarrow \mathrm{perm}_{p'}\Bigl((S_{\mathrm{old}}\oplus x)\oplus x\Bigr)\;=\;\mathrm{perm}_{p'}(S_{\mathrm{old}})
\]

Despite permutations, one can recover \(x\) and then \(S_{\mathrm{old}}\equiv f\) by observing many leaks. The solution rests on three key insights:

1. **Column-wise consistency**: Each leak byte at position \(k\) satisfies  
   \[
   \mathrm{Leak}_i[k]\;=\;f\bigl(p_i(k)\bigr)\;\oplus\;x[k],\quad i=1,\dots,N,\;k=0,\dots,63.
   \]
2. **Mode-XOR extraction**: For any two columns \(a,b\), consider all pairwise XORs  
   \[
   \{\mathrm{Leak}_i[a]\oplus\mathrm{Leak}_j[b]\;|\;1\le i,j\le N\}.
   \]
   Exactly 64 pairs satisfy \(p_i(a)=p_j(b)\), yielding  
   \[
   (f[j]\oplus x[a])\oplus(f[j]\oplus x[b]) \;=\; x[a]\oplus x[b].
   \]
   Hence the **mode** of those \(N^2\) XORs equals \(x[a]\oplus x[b]\).
3. **Equivalence clustering**: Whenever \(\mathrm{Leak}_i[k]=\mathrm{Leak}_j[k]\), we have  
   \[
   f\bigl(p_i(k)\bigr)\oplus x[k] \;=\; f\bigl(p_j(k)\bigr)\oplus x[k]\quad\Longrightarrow\quad p_i(k)=p_j(k).
   \]
   Grouping all such collisions across \(i\) identifies exactly 64 equivalence classes, each corresponding to one flag byte index.

---

## Method Overview

1. **Collect \(N\) leaks**: build an \(N\times 64\) table \(\mathrm{Leak}_i[k]\).  
2. **Compute mask differences**:
   - Fix a reference column \(0\).  
   - For each \(b=1,\dots,63\), form set \(\{\mathrm{Leak}_i[0]\oplus\mathrm{Leak}_j[b]\}\).  
   - The mode of that set is \(x[0]\oplus x[b]\).  
   - By choosing \(x[0]=0\), recover \(x[b]\) for all \(b\).
3. **Unmask leaks**:
   \[
   V_i[k] \;=\; \mathrm{Leak}_i[k]\;\oplus\;x[k] \;=\; f\bigl(p_i(k)\bigr)\oplus C,
   \]
   where \(C\) is a single unknown byte constant.
4. **Cluster positions**: unite \((i,k)\) and \((j,k)\) whenever \(V_i[k]=V_j[k]\).  This yields exactly 64 clusters corresponding to \(f[0],\dots,f[63]\).
5. **Reconstruct flag**: using any row \(i\), assign each unmasked value to its cluster index to fill the 64-byte array \(\{f[j]\oplus C\}\).
6. **Fix global constant**: try all 256 values for \(C\) so that the resulting 64-byte string is valid ASCII (e.g.\ matching `flag{…}`).

---

## Core Formulas

- **Leak formula**:  
  \[
    \mathrm{Leak}_i[k] = f\bigl(p_i(k)\bigr)\;\oplus\;x[k].
  \]
- **Mode XOR**:  
  \[
    x[a]\oplus x[b] = \operatorname{mode}\bigl\{\mathrm{Leak}_i[a]\oplus\mathrm{Leak}_j[b]\bigr\}.
  \]
- **Collision clustering**:  
  \[
    \mathrm{Leak}_i[k]=\mathrm{Leak}_j[k]\;\Longrightarrow\;p_i(k)=p_j(k).
  \]

By following these steps and applying these formulas, one recovers the full 64-byte flag in a few hundred queries.
