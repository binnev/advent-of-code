// imports the "loading" submodule here, but does not expose it to parents
mod loading;
mod sparse_matrix;

// loads and exposes all the contents of the loading module. They will be
// accessible via crate::utils::load_puzzle_input, for example.
// I guess this is equivalent to python's `from .loading import *`
pub use loading::*;

