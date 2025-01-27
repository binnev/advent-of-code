// imports the "loading" submodule here, but does not expose it to parents
mod loading;
mod sparse_matrix;

// loads and exposes all the contents of the loading module. They will be
// accessible via crate::utils::load_puzzle_input, for example.
// I guess this is equivalent to python's `from .loading import *`
pub use loading::*;
pub use sparse_matrix::{Coord, Direction, SparseMatrix};

// Useful for drawing
pub mod shade {
    pub const LIGHT: char = '░';
    pub const MEDIUM: char = '▒';
    pub const DARK: char = '▓';
    pub const FULL: char = '█';
}

/// Given a path to a function like `y2024::day1::part1`, expand it to the path
/// plus the stringified version of it:
///     (y2024::day1::part1, "y2024::day1::part1")
///
/// Useful for DRYing up test cases.
#[macro_export]
macro_rules! expand {
    ($path:path) => {
        ($path, stringify!($path))
    };
}
/// "y2024::day1::part1" -> ("2024", "day1", "part1")
pub fn split_path(name: &str) -> (&str, &str, &str) {
    let parts: Vec<_> = name.split("::").collect();
    let year = parts[0].trim_start_matches("y");
    let day = parts[1];
    let part = parts[2];
    (year, day, part)
}
