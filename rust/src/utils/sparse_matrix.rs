use std::{
    collections::HashMap,
    fmt::Display,
    ops::{Deref, DerefMut},
};

pub type Coord = (i64, i64);

#[derive(PartialEq, Eq, Debug)]
pub struct SparseMatrix<T> {
    pub contents: HashMap<Coord, T>,
}
impl<T> SparseMatrix<T> {
    pub fn new() -> Self {
        Self {
            contents: HashMap::new(),
        }
    }
    pub fn xs(&self) -> impl Iterator<Item = i64> + '_ {
        self.contents
            .iter()
            .map(|(coord, _)| coord.0)
    }
    pub fn ys(&self) -> impl Iterator<Item = i64> + '_ {
        self.contents
            .iter()
            .map(|(coord, _)| coord.1)
    }
}
/// This allows us to call the HashMap methods directly on the SparseMatrix.
/// E.g.:
///
///     let matrix = SparseMatrix::new();
///     matrix.insert(coord, '#');
impl<T> Deref for SparseMatrix<T> {
    type Target = HashMap<Coord, T>;
    fn deref(&self) -> &Self::Target {
        &self.contents
    }
}
impl<T> DerefMut for SparseMatrix<T> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.contents
    }
}
impl<T: Display> Display for SparseMatrix<T> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let xmin = self.xs().min().unwrap_or(0);
        let xmax = self.xs().max().unwrap_or(0);
        let ymin = self.ys().min().unwrap_or(0);
        let ymax = self.ys().max().unwrap_or(0);
        let stringified = (ymin..ymax + 1)
            .map(|y| {
                let line: String = (xmin..xmax + 1)
                    .map(|x| {
                        self.get(&(x, y))
                            .map(|val| format!("{val}")) // use the value's Display
                            .unwrap_or(" ".into()) // or default to empty space
                    })
                    .collect();
                line
            })
            .collect::<Vec<_>>()
            .join("\n");
        write!(f, "{stringified}")?;
        Ok(())
    }
}
impl From<&str> for SparseMatrix<char> {
    fn from(value: &str) -> Self {
        let mut contents = HashMap::new();
        for (y, line) in value.lines().enumerate() {
            for (x, ch) in line.chars().enumerate() {
                let coord = (x as i64, y as i64);
                contents.insert(coord, ch);
            }
        }
        Self { contents }
    }
}

// Get the vertical and horizontal neighbours (no diagonals)
pub fn coord_neighbours(coord: &Coord) -> Vec<Coord> {
    let (x, y) = coord.clone();
    vec![(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
}

#[cfg(test)]
mod tests {
    use super::*;
    const EXAMPLE: &str = "....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
......O.#.
#.........
......#...";

    #[test]
    fn test_from_str_empty() {
        let input = "";
        let matrix: SparseMatrix<char> = input.into();
        assert_eq!(matrix.len(), 0);
    }

    #[test]
    fn test_from_str() {
        let matrix: SparseMatrix<char> = EXAMPLE.into();
        assert_eq!(matrix.len(), 100);
        assert_eq!(matrix.contents.get(&(4, 0)), Some(&'#'));
    }

    #[test]
    fn test_display() {
        let matrix: SparseMatrix<char> = EXAMPLE.into();
        let s = format!("{matrix}");
        assert_eq!(s, EXAMPLE)
    }

    /// Check that we can access the HashMap methods directly on SparseMatrix
    #[test]
    fn test_deref() {
        let mut matrix = SparseMatrix::new();
        assert_eq!(
            matrix.len(), // gets rerouted to matrix.contents.len()
            0
        );
        let previous = matrix.insert((69, 420), 'x'); // matrix.contents.insert
        assert_eq!(previous, None);
        assert_eq!(matrix.len(), 1);
    }
}
