use std::{ptr, sync::Arc, thread};
use std::sync::atomic::{AtomicPtr, Ordering::*};

struct Node { value: u64, next: *mut Node }
struct Stack { head: AtomicPtr<Node> }

impl Stack {
    fn push(&self, value: u64) {
        let new = Node { value, next: ptr::null_mut() };
        let node = Box::into_raw(Box::new(new));
        loop {
            let head = self.head.load(Acquire);  // 1. look at the top plate
            unsafe { (*node).next = head; }      // 2. our plate sits on it
            // 3. swap in our plate, only if the top is still `head`
            if self.head.compare_exchange_weak(head, node, Release, Relaxed)
                .is_ok() { return; }
        }                                        // top changed: retry
    }
    fn pop(&self) -> Option<u64> {
        loop {
            let head = self.head.load(Acquire);  // 1. look at the top plate
            if head.is_null() { return None; }   // no plates left
            let next = unsafe { (*head).next };  // 2. the plate under it
            // 3. make `next` the top, only if the top is still `head`
            if self.head.compare_exchange_weak(head, next, AcqRel, Relaxed)
                .is_ok() {
                // it's ours. (This demo never frees nodes: see ABA.)
                return Some(unsafe { (*head).value });
            }
        }
    }
}
fn main() {
    let stack = Arc::new(Stack { head: AtomicPtr::new(ptr::null_mut()) });
    let pushers: Vec<_> = (0..4u64).map(|t| {
        let s = Arc::clone(&stack);
        thread::spawn(move || for i in 0..100_000 { s.push(t * 100_000 + i) })
    }).collect();
    for h in pushers { h.join().unwrap(); }
    let poppers: Vec<_> = (0..4).map(|_| {
        let s = Arc::clone(&stack);
        thread::spawn(move || {
            let mut n = 0u64;
            while s.pop().is_some() { n += 1 }
            n
        })
    }).collect();
    let popped: u64 = poppers.into_iter().map(|h| h.join().unwrap()).sum();
    let empty = stack.pop().is_none();
    println!("pushed 400000, popped {popped}, empty now: {empty}");
}
