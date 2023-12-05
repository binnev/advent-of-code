// this is an import.
// Rust automatically creates a namespace
// all files are modules.
// all folders are also modules.
// Here we are basically declaring "this module exists"
mod puzzles;

// crate refers to the root of the module tree.
// by default all members of a module are private -- visible only within the
// module.
// unit tests that test private members must be part of the same module (like
// packages in Go)
// Here we actually specify what we want to import from the module
use crate::puzzles::y2023::day1::part1;

fn main() {
    let result = part1();
    println!("{}", result);
}
