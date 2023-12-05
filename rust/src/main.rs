// this is an import.
// Rust automatically creates a namespace
// all files are modules.
// all folders are also modules.
// Here we are basically declaring "this module exists"
mod foo;

mod prelude {
    // create module inline
    pub use crate::foo::{Another, MyStruct};
}
use crate::prelude::*; // make the types exposed in the prelude available

// crate refers to the root of the module tree.

// by default all members of a module are private -- visible only within the
// module.

// unit tests that test private members must be part of the same module (like
// packages in Go)

// Here we actually specify what we want to import from the module
use crate::foo::{Another, MyStruct};

fn main() {
    let _ms = MyStruct {};
    let _a = Another {};
}
