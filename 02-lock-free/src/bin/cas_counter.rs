use std::sync::{Arc, atomic::{AtomicU64, Ordering::Relaxed}};
use std::thread;

fn add_one(board: &AtomicU64, retries: &AtomicU64) {
    let mut seen = board.load(Relaxed);  // 1. read the board
    loop {
        // 2. "write seen + 1, but only if it still says seen"
        match board.compare_exchange_weak(seen, seen + 1, Relaxed, Relaxed) {
            Ok(_) => return,         // it did: done
            Err(now) => {            // it changed: retry
                seen = now;
                retries.fetch_add(1, Relaxed);
            }
        }
    }
}
fn main() {
    let board = Arc::new(AtomicU64::new(0));
    let retries = Arc::new(AtomicU64::new(0));
    let handles: Vec<_> = (0..8).map(|_| {
        let (b, r) = (Arc::clone(&board), Arc::clone(&retries));
        thread::spawn(move || for _ in 0..1_000_000 { add_one(&b, &r) })
    }).collect();
    for h in handles { h.join().unwrap(); }
    println!("counter = {}", board.load(Relaxed));
    println!("retries = {}", retries.load(Relaxed));
}
