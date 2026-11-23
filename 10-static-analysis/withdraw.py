def withdraw_buggy(balance, amount):
    return balance - amount              # can go negative

def withdraw_ok(balance, amount):
    if amount > balance:
        return balance                   # refuse; leave the balance as is
    return balance - amount

def check(fn, balances, amounts):
    failures = []
    for b in balances:
        for a in amounts:
            result = fn(b, a)
            if result < 0:
                failures.append((b, a, result))
    return failures

balances = list(range(0, 11))            # 0..10
amounts = list(range(0, 11))

# a few handwritten tests (easy cases)
hand = [(10, 3), (10, 0), (5, 5)]
print("handwritten tests:")
for b, a in hand:
    print(f"  withdraw({b}, {a}) buggy={withdraw_buggy(b, a)} ok={withdraw_ok(b, a)}")

buggy = check(withdraw_buggy, balances, amounts)
ok = check(withdraw_ok, balances, amounts)
print(f"exhaustive check: {len(balances)} balances x {len(amounts)} amounts",
      f"= {len(balances) * len(amounts)} cases")
print(f"buggy failures: {len(buggy)}, first few: {buggy[:3]}")
print(f"ok failures: {len(ok)}")
