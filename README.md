# Systems Programming Explained
## Advanced Programming Concepts Made Easy

Small, runnable examples from David Oluyale's Agentic AI Hub video series. Everyday analogies first, then real code and measured results.

| Part | Tutorial | Code |
|---|---|---|
| 1 | [Make Your Python Code 20x Faster (Threads vs Processes Explained)](https://youtu.be/dLdfrp02n6A) | [Threads, processes, locks and asyncio](01-threads-vs-processes/) |
| 2 | [Lock-Free Code Explained: How Fast Programs Share Data Without Locks](https://youtu.be/FL4Ts9LfBJk) | [Atomics, CAS, a lock-free stack and memory ordering (Rust)](02-lock-free/) |
| 3 | [Why Concurrent Programs Break: Race Conditions, Deadlocks and Linearizability](https://youtu.be/2NCCn2o42EA) | [Races, deadlocks and a linearizability checker (Python + Rust)](03-race-conditions/) |
| 4 | [Distributed Systems Explained: Consensus, Replication, Transactions and Idempotency](https://youtu.be/fni53-4dPGk) | [Idempotency keys, SQLite transactions and a 3-node majority cluster (Python)](04-distributed-systems/) |
| 5 | [How Databases Survive Crashes: Write-Ahead Logs and Recovery Explained](https://youtu.be/-l_xC6ECaoc) | [A write-ahead log, torn-write recovery, fsync timing and checkpoints (Python)](05-database-internals/) |
| 6 | How Programming Languages Work: Compilers, Parsers, Interpreters and VMs | [A tiny lexer, parser, interpreter and stack VM for 2 + 3 * 4 (Python)](06-compilers/) |
| 7 | Systems Programming Explained: Memory, Allocators, File Formats and Protocols | [A tiny binary format, a bump allocator (Python + a short C demo), and a socket protocol](07-low-level-systems/) |
| 8 | How Compression Works: DEFLATE, Huffman and LZ77 Explained | [Run-length encoding, a tiny LZ77-style pointer, Huffman codes, and zlib DEFLATE (Python)](08-compression/) |
| 9 | Make Programs Faster: Profiling, Caches and Vectorization Explained | [cProfile, row vs column sums, and a Python loop vs a NumPy add](09-performance/) |
| 10 | Catch Bugs Before You Run: Types, Static Analysis and Program Verification | [mypy on a typed greet, a 20-line AST linter, and exhaustive checks of withdraw (Python)](10-static-analysis/) |

This is the complete companion-code set for the ten-video series.

- [Playlist](https://www.youtube.com/playlist?list=PLZaDePzkCIxo)
- [Agentic AI Hub](https://www.youtube.com/@AgenticAIHub1)
- [Python Crash Course](https://youtu.be/ZaY_l07IZSo)

All measurements are from actual runs, not universal promises. Read each part's README for the test conditions.
