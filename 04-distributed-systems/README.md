# Part 4: Distributed Systems Explained

Companion code for the video **"Distributed Systems Explained: Consensus, Replication, Transactions and Idempotency"** from the *Systems Programming Explained* series by David Oluyale (Agentic AI Hub).

- Video 1: https://youtu.be/dLdfrp02n6A
- Video 2: https://youtu.be/FL4Ts9LfBJk
- Video 3: https://youtu.be/2NCCn2o42EA
- Playlist: https://www.youtube.com/playlist?list=PLZaDePzkCIxo

## The ideas in everyday terms

Three offices share one customer book. Phone lines can drop, and an office can lose power.

- **Replication:** keep a copy of the book in every office, so one fire doesn't lose the data.
- **Consensus:** the offices agree on the next entry, by majority, even if some phones die.
- **Transaction:** a transfer finishes in both accounts, or not at all.
- **Idempotency:** pressing the lift button twice still calls one lift. A retried payment must not charge twice.

## What's in here

| File | What it shows |
|---|---|
| `payments.py` | A payment whose reply is lost (**simulated**, in memory, no real money). Retrying without a key charges twice; with an idempotency key, once |
| `transfer_db.py` | A transfer in a real SQLite database. The transfer runs in a child process killed with `os._exit(1)` between the debit and the credit. Without a transaction money vanishes; with `BEGIN`/`COMMIT` it rolls back |
| `node.py` | One replica: a tiny HTTP server that stores `[version, value]` per key in memory and in its own JSON file |
| `cluster.py` | Starts 3 nodes as 3 local processes, writes with majority (2 of 3) acks, stops nodes, shows a stale read and a catch-up |

Standard library only.

## Run it

```bash
cd 04-distributed-systems
python3 payments.py
python3 transfer_db.py   # creates bank.db in this folder
python3 cluster.py       # uses ports 8001-8003 on 127.0.0.1 and a fresh temp folder
```

## Observed results from the video

Recorded on 2026-11-22 at 23:36 WAT with CPython 3.13.5 on an 8-CPU Intel Xeon Linux machine. Each result is one run of the exact code in this folder (see `recorded_outputs.json`).

| Demo | Result |
|---|---|
| `payments.py`, no key | 1 lost reply, 1 retry: charged 2 times, total $40 |
| `payments.py`, idempotency key | same retry: charged 1 time, total $20 |
| `transfer_db.py`, no transaction, crash | exit code 1: Ada 70, Bob 100, total 170 |
| `transfer_db.py`, transaction, crash | exit code 1: Ada 100, Bob 100, total 200 |
| `transfer_db.py`, transaction, no crash | exit code 0: Ada 70, Bob 130, total 200 |
| `cluster.py`, all 3 up | write pizza: 3/3 acks, OK (0.02 s) |
| `cluster.py`, node 3 down | write sushi: 2/3 acks, OK (0.00 s) |
| `cluster.py`, node 3 restarted | node 3 says `[1, 'pizza']` (stale); majority says `[2, 'sushi']`; after catch-up node 3 says `[2, 'sushi']` |
| `cluster.py`, nodes 2 and 3 down | write tacos: 1/3 acks, FAILED (0.00 s) |

## Notes and honest caveats

- **The cluster is simulated on one machine.** The three nodes are separate processes talking HTTP over `127.0.0.1`. A stopped node refuses connections at once, so failed sends took about 0 s. Across a real network, you'd often wait for the 0.5 s timeout instead.
- **It's a toy quorum, not consensus.** There's one writer, no leader election and no ordered log. A failed write can stay on a node: node 1 kept `tacos` even though the write FAILED. Real systems use Raft or Paxos (for example, etcd in Kubernetes). Don't use this as a database.
- **Majority reads** overlap with any majority write, which is why they return the newest acknowledged version here.
- **The payment network failure is simulated** (the reply is dropped on the first attempt). The idempotency keys live in memory. In production, store the key and the payment together in one transaction, with a unique constraint on the key.
- **The SQLite crash kills the process**, not the machine's power. It shows SQLite rolling back an uncommitted transaction when the database is next opened. It isn't a power-loss durability test.
