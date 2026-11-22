use std::sync::atomic::{AtomicI64, AtomicUsize, Ordering::SeqCst};
use std::sync::Arc;
use std::thread;

// Check, then act. Each step is atomic, but the pair is not.
fn withdraw(bal: &AtomicI64, amount: i64) {
    if bal.load(SeqCst) >= amount {
        bal.fetch_sub(amount, SeqCst);
    }
}

// CAS: take the money only if the balance hasn't changed.
fn safe_withdraw(bal: &AtomicI64, amount: i64) {
    let mut seen = bal.load(SeqCst);
    while seen >= amount {
        match bal.compare_exchange(seen, seen - amount, SeqCst, SeqCst) {
            Ok(_) => return,
            Err(now) => seen = now,
        }
    }
}

fn trials(f: fn(&AtomicI64, i64)) -> u32 {
    let mut negative = 0;
    for _ in 0..20_000 {
        let bal = Arc::new(AtomicI64::new(100));
        let ready = Arc::new(AtomicUsize::new(0));
        let people: Vec<_> = (0..2).map(|_| {
            let (bal, ready) = (bal.clone(), ready.clone());
            thread::spawn(move || {
                ready.fetch_add(1, SeqCst);      // at the start line
                while ready.load(SeqCst) < 2 {}  // wait for the other
                f(&bal, 80);
            })
        }).collect();
        for p in people { p.join().unwrap(); }
        if bal.load(SeqCst) < 0 { negative += 1; }
    }
    negative
}

fn main() {
    println!("withdraw:      {} of 20000 went negative", trials(withdraw));
    println!("safe_withdraw: {} of 20000 went negative", trials(safe_withdraw));
}
