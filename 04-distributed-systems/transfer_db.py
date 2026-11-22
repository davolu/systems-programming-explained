import os, sqlite3, multiprocessing as mp

DB = "bank.db"
TAKE = "UPDATE acct SET money = money - ? WHERE name = ?"
GIVE = "UPDATE acct SET money = money + ? WHERE name = ?"

def setup():
    db = sqlite3.connect(DB)
    db.execute("CREATE TABLE IF NOT EXISTS acct (name TEXT, money INT)")
    db.execute("DELETE FROM acct")
    db.executemany("INSERT INTO acct VALUES (?, ?)",
                   [("Ada", 100), ("Bob", 100)])
    db.commit(); db.close()

def transfer(amount, use_transaction, crash):
    db = sqlite3.connect(DB, isolation_level=None)  # we control commits
    if use_transaction: db.execute("BEGIN")
    db.execute(TAKE, (amount, "Ada"))
    if crash: os._exit(1)                           # the power goes out!
    db.execute(GIVE, (amount, "Bob"))
    if use_transaction: db.execute("COMMIT")

def balances():
    db = sqlite3.connect(DB)
    rows = dict(db.execute("SELECT name, money FROM acct"))
    db.close()
    return f"Ada {rows['Ada']}, Bob {rows['Bob']}, total {sum(rows.values())}"

for use_transaction, crash in ((False, True), (True, True), (True, False)):
    setup()
    p = mp.Process(target=transfer, args=(30, use_transaction, crash))
    p.start(); p.join()
    print(f"transaction={use_transaction}, crash={crash}:",
          f"exit code {p.exitcode} -> {balances()}")
