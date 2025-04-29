# NYT CTF - Sudoku

## Challenge Description

> *"Try this numbers game, minus the math."*

This succinct tagline hints that while the challenge looks like a math puzzle (and is themed like Sudoku), it does **not** require arithmetic or logic in the traditional Sudoku sense. Instead, it's a constraint puzzle cloaked in numeric form.

## Challenge Overview

The "Sudoku" challenge was accessed via a netcat (`nc`) connection. Upon initial random input, the server responded with a structured set of constraints — strongly implying a Constraint Satisfaction Problem (CSP).

Despite its name, it was **not a standard Sudoku**. Instead, it involved:

- **81 integer variables** (`s0` through `s80`), mimicking a 9x9 grid.
- Each variable must be an integer between **1 and 9**, noticed from the mentioned constraints.
- A **chain of value constraints** using both equality and inequality (e.g., `s[68] > s[58] == s[26]`).
- A **long chain of inequality constraints**: several hundred `s[a] != s[b]` rules connecting many variables.

## Strategy

The structure of the constraints made it an ideal candidate for symbolic solving. The approach:

1. **Declare** the 81 integer variables using Z3’s `Ints`.
2. **Add domain constraints**: ensure values are between 1 and 9.
3. **Model the equality and inequality chain** exactly as received from the challenge.
4. **Solve** the model using Z3.
5. **Verify** that the solution satisfies all original constraints.

## Solution

The Z3 SMT solver produced a valid assignment — a list of 81 digits satisfying all the constraints. This result was confirmed with assertions re-checking the entire constraint set.

The final output was a single 81-digit string — an input to be sent back to the server.

