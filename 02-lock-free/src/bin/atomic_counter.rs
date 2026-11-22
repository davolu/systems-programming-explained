use std::sync::{Arc, atomic::{AtomicU64, Ordering}};
use std::{env, thread, time::Instant};

fn main() {
    let threads: u64 = env::args().nth(1).map_or(8, |s| s.parse().unwrap());
    let counter = Arc::new(AtomicU64::new(0));
    let start = Instant::now();
    let handles: Vec<_> = (0..threads).map(|_| {
        let c = Arc::clone(&counter);
        thread::spawn(move || {
            for _ in 0..8_000_000 / threads {
                c.fetch_add(1, Ordering::Relaxed); // one unbreakable step
            }
        })
    }).collect();
    for h in handles { h.join().unwrap(); }
    let ms = start.elapsed().as_secs_f64() * 1000.0;
    let total = counter.load(Ordering::Relaxed);
    println!("Atomic, {threads} threads: {total} in {ms:.0} ms");
}
