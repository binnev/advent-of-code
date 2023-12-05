// pub means public -- we expose this member to the world outside this module
// I think this is python equivalent of `from . import another`
// pub mod another;

// this is a private import
mod another;

// python equiv: from .another import Another
pub use another::Another;
pub struct MyStruct {}
