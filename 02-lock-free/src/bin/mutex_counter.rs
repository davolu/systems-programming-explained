use std::sync::{Arc, Mutex};
use std::{env, thread, time::Instant};

fn main() {
    let threads: u64 = env::args().nth(1).map_or(8, |s| s.parse().unwrap());
    let counter = Arc::new(Mutex::new(0u64));
    let start = Instant::now();
    let handles: Vec<_> = (0..threads).map(|_| {
        let c = Arc::clone(&counter);
        thread::spawn(move || {
            for _ in 0..8_000_000 / threads {
                *c.lock().unwrap() += 1; // take key, add 1, give key back
            }
        })
    }).collect();
    for h in handles { h.join().unwrap(); }
    let ms = start.elapsed().as_secs_f64() * 1000.0;
    let total = *counter.lock().unwrap();
    println!("Mutex,  {threads} threads: {total} in {ms:.0} ms");
}
