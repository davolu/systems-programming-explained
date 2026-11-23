# Part 6: How Programming Languages Work

Companion code for the video **"How Programming Languages Work: Compilers, Parsers, Interpreters and VMs"** from the *Systems Programming Explained* series by David Oluyale (Agentic AI Hub).

- Video 1: https://youtu.be/dLdfrp02n6A
- Video 2: https://youtu.be/FL4Ts9LfBJk
- Video 3: https://youtu.be/2NCCn2o42EA
- Video 4: https://youtu.be/fni53-4dPGk
- Video 5: https://youtu.be/-l_xC6ECaoc
- Playlist: https://www.youtube.com/playlist?list=PLZaDePzkCIxo

## The ideas in everyday terms

Source code is a recipe written in English.

- **Lexer:** splits the sentence into words, called tokens.
- **Parser:** checks the grammar and builds a family tree (an abstract syntax tree). Times binds tighter than plus, because of how the grammar is layered.
- **Interpreter:** a cook who walks that tree, step by step, and gives you the dish now.
- **Compiler + virtual machine:** translate the tree into a short list of instructions (bytecode), then run them on a standard kitchen (a stack machine).

## What's in here

| File | What it shows |
|---|---|
| `parse_expr.py` | A tiny lexer and recursive-descent parser for `+`, `*`, numbers and brackets. Prints tokens and a tree for `2 + 3 * 4` |
| `interpret_expr.py` | Walks the tree to compute `2 + 3 * 4` and `(2 + 3) * 4` |
| `vm_expr.py` | Compiles the same tree to `PUSH` / `MUL` / `ADD` and runs it on a small stack machine |

The lexer and parser helpers are copied into the second and third files so each one runs on its own. Standard library only (Python 3.8+).

## Run it

```bash
cd 06-compilers
python3 parse_expr.py
python3 interpret_expr.py
python3 vm_expr.py
```

## Observed results from the video

Recorded on 2026-11-23 at 11:45 WAT with CPython 3.13.5 on an 8-CPU Intel Xeon Linux cloud machine. Each result is one run of the exact code in this folder (see `recorded_outputs.json`).

| Demo | Result |
|---|---|
| `parse_expr.py` tokens for `2 + 3 * 4` | `NUMBER 2`, `PLUS +`, `NUMBER 3`, `STAR *`, `NUMBER 4`, `EOF` |
| `parse_expr.py` tree | `+` at the top, left child `2`, right child `*` of `3` and `4` |
| `interpret_expr.py` | `2 + 3 * 4 = 14`, `(2 + 3) * 4 = 20` |
| `vm_expr.py` bytecode | `PUSH 2`, `PUSH 3`, `PUSH 4`, `MUL`, `ADD` |
| `vm_expr.py` run | stack goes `[2]`, `[2, 3]`, `[2, 3, 4]`, `[2, 12]`, `[14]`; result `14` |

## Notes and honest caveats

- This is a toy language: no variables, no precedence table beyond the expr/term split, and only `+` and `*`.
- A real compiler does a lot more (types, scopes, optimisation, more instructions). The path is the same: text, tokens, tree, then walk or translate.
- CPython, the JVM, .NET and many JavaScript engines compile to bytecode and run it on a virtual machine. SQL, JSON and config files have parsers too.
