use std::sync::{Arc, atomic::{AtomicBool, AtomicU64, Ordering::*}};
use std::thread;

fn main() {
    let meal = Arc::new(AtomicU64::new(0));
    let bell = Arc::new(AtomicBool::new(false));
    let (m, b) = (Arc::clone(&meal), Arc::clone(&bell));
    let cook = thread::spawn(move || {
        m.store(42, Relaxed);    // 1. put the meal on the counter
        b.store(true, Release);  // 2. ring the bell: all of step 1 is visible
    });
    while !bell.load(Acquire) {} // waiter: wait for the bell
    println!("bell rang, meal = {}", meal.load(Relaxed));
    cook.join().unwrap();
}
