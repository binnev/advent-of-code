use std::{
    collections::HashMap,
    fmt::Display,
    ops::{Deref, DerefMut},
};

#[derive(PartialEq, Eq, Hash, Debug, Clone, Copy)]
pub struct Coord(pub i64, pub i64);
impl Coord {
    pub fn west(&self) -> Self {
        self.neighbour(West)
    }
    pub fn east(&self) -> Self {
        self.neighbour(East)
    }
    pub fn north(&self) -> Self {
        self.neighbour(North)
    }
    pub fn south(&self) -> Self {
        self.neighbour(South)
    }
    pub fn neighbour(&self, direction: Direction) -> Self {
        self.translate(direction, 1)
    }
    pub fn translate(&self, direction: Direction, steps: i64) -> Self {
        use Direction::*;
        let (x, y) = self.into();
        match direction {
            East => Coord(x + steps, y),
            West => Coord(x - steps, y),
            North => Coord(x, y - steps), // NOTE: y is positive down
            South => Coord(x, y + steps),
        }
    }
    // Get the vertical and horizontal neighbours (no diagonals)
    pub fn neighbours(&self) -> Vec<Self> {
        let (x, y) = self.into();
        vec![
            Coord(x + 1, y),
            Coord(x - 1, y),
            Coord(x, y + 1),
            Coord(x, y - 1),
        ]
    }
    pub fn neighbours_all(&self) -> Vec<Self> {
        let mut out = vec![];
        for x in [-1, 0, 1] {
            for y in [-1, 0, 1] {
                if (x, y) == (0, 0) {
                    continue;
                }
                out.push((x, y).into());
            }
        }
        out
    }
    /// Return the taxicab distance (number of steps in x and y) from self to
    /// other.
    pub fn taxicab_dist_to(&self, other: &Coord) -> u64 {
        let dx = self.0.abs_diff(other.0);
        let dy = self.1.abs_diff(other.1);
        dx + dy
    }

    /// Use the formula for Pascal's Triangle to calculate the number of unique
    /// paths from `self` to `other`. This assumes movemement happens using only
    /// horizontal/vertical steps (no diagonals)
    pub fn num_unique_paths_to(&self, other: &Coord) -> u64 {
        if other == self {
            return 0; // there are no paths from self to self
        }
        let delta = *other - *self;
        let m = delta.0.abs() as u64;
        let n = delta.1.abs() as u64;
        let numerator = factorial(m + n);
        let denominator = factorial(m) * factorial(n);
        numerator / denominator
    }
}
impl std::ops::Add for Coord {
    type Output = Self;
    fn add(self, rhs: Self) -> Self::Output {
        Self(self.0 + rhs.0, self.1 + rhs.1)
    }
}
impl std::ops::Sub for Coord {
    type Output = Self;
    fn sub(self, rhs: Self) -> Self::Output {
        self + Coord(-rhs.0, -rhs.1)
    }
}
impl From<(i64, i64)> for Coord {
    fn from(value: (i64, i64)) -> Self {
        Self(value.0, value.1)
    }
}
impl From<&(i64, i64)> for Coord {
    fn from(value: &(i64, i64)) -> Self {
        value.clone().into()
    }
}
impl Into<(i64, i64)> for Coord {
    fn into(self) -> (i64, i64) {
        (self.0, self.1)
    }
}
impl Into<(i64, i64)> for &Coord {
    fn into(self) -> (i64, i64) {
        self.clone().into()
    }
}

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
    pub fn limits(&self) -> ((i64, i64), (i64, i64)) {
        let mut iter = self.keys();
        let (mut xmin, mut xmax) = iter
            .next()
            .expect("Can't get limits of empty SparseMatrix!")
            .into();
        let (mut ymin, mut ymax) = (xmin, xmax).clone();
        for xy in iter {
            let (x, y) = xy.into();
            if x < xmin {
                xmin = x
            }
            if x > xmax {
                xmax = x
            }
            if y < ymin {
                ymin = y
            }
            if y > ymax {
                ymax = y
            }
        }
        ((xmin, xmax), (ymin, ymax))
    }
}
impl<T: Clone> SparseMatrix<T> {
    /// Insert the same value at many Coords. The `IntoIterator` makes it such
    /// that we can pass a Vec<Coord> but also a HashSet<Coord>.
    pub fn insert_many(
        &mut self,
        coords: impl IntoIterator<Item = Coord>,
        value: T,
    ) {
        for coord in coords {
            self.insert(coord.clone(), value.clone());
        }
    }
}
impl<T: PartialEq> SparseMatrix<T> {
    /// Get the coord of the given value, if the value is present
    pub fn locate(&self, needle: T) -> Option<&Coord> {
        self.iter().find_map(
            |(coord, value)| {
                if value == &needle {
                    Some(coord)
                } else {
                    None
                }
            },
        )
    }
}
/// This allows us to call the HashMap methods directly on the SparseMatrix.
/// E.g.:
///
/// let matrix = SparseMatrix::new();
/// matrix.insert(coord, '#');
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
                        self.get(&(x, y).into())
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
                let coord = Coord(x as i64, y as i64);
                contents.insert(coord, ch);
            }
        }
        Self { contents }
    }
}

#[derive(PartialEq, Eq, Debug, Clone, Copy, Hash)]
pub enum Direction {
    North,
    East,
    South,
    West,
}
use Direction::*;

use super::factorial;
impl Direction {
    pub fn is_horizontal(&self) -> bool {
        match self {
            East | West => true,
            _ => false,
        }
    }
    pub fn clockwise(&self) -> Self {
        match self {
            North => East,
            East => South,
            South => West,
            West => North,
        }
    }
    pub fn counter_clockwise(&self) -> Self {
        match self {
            North => West,
            West => South,
            South => East,
            East => North,
        }
    }
    pub fn char(&self) -> char {
        match self {
            East => '>',
            West => '<',
            North => '^',
            South => 'v',
        }
    }
}
impl Display for Direction {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.char())
    }
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
        assert_eq!(matrix.contents.get(&(4, 0).into()), Some(&'#'));
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
        let previous = matrix.insert((69, 420).into(), 'x'); // matrix.contents.insert
        assert_eq!(previous, None);
        assert_eq!(matrix.len(), 1);
    }

    #[test]
    fn test_locate() {
        let matrix: SparseMatrix<char> = EXAMPLE.into();
        assert_eq!(matrix.locate('O'), Some(&Coord(6, 7)));
        // If there are multiple #s, it will return a random one
        assert!(matrix.locate('#').is_some());
        assert_eq!(matrix.locate('X'), None);
    }

    #[test]
    fn test_num_unique_paths_to() {
        for (from, to, expected) in [
            // ----- edge case -----
            (Coord(0, 0), Coord(0, 0), 0),
            // ----- 1 path -----
            (Coord(0, 0), Coord(0, 1), 1),
            (Coord(0, 0), Coord(1, 0), 1),
            (Coord(0, 0), Coord(0, -1), 1),
            (Coord(0, 0), Coord(-1, 0), 1),
            (Coord(0, 1), Coord(0, 0), 1),
            (Coord(1, 0), Coord(0, 0), 1),
            (Coord(0, -1), Coord(0, 0), 1),
            (Coord(-1, 0), Coord(0, 0), 1),
            // nonzero start point
            (Coord(2, 3), Coord(2, 4), 1),
            (Coord(2, 3), Coord(2, 2), 1),
            (Coord(2, 3), Coord(1, 3), 1),
            (Coord(2, 3), Coord(3, 3), 1),
            // straight paths longer than 1 also have 1 unique path
            (Coord(0, 0), Coord(0, 2), 1),
            (Coord(0, 0), Coord(0, -2), 1),
            (Coord(0, 0), Coord(2, 0), 1),
            (Coord(0, 0), Coord(-2, 0), 1),
            // ----- 2 paths -----
            (Coord(0, 0), Coord(1, 1), 2),
            (Coord(0, 0), Coord(-1, -1), 2),
            (Coord(1, 1), Coord(0, 0), 2),
            (Coord(1, -1), Coord(0, 0), 2),
            // ----- 3 paths -----
            (Coord(0, 0), Coord(1, 2), 3),
            (Coord(0, 0), Coord(1, -2), 3),
            (Coord(0, 0), Coord(-1, 2), 3),
            (Coord(0, 0), Coord(-1, -2), 3),
            // ----- more -----
            (Coord(0, 0), Coord(3, 4), 35),
            (Coord(0, 0), Coord(4, 3), 35),
            (Coord(3, 4), Coord(0, 0), 35),
            (Coord(4, 3), Coord(0, 0), 35),
        ] {
            let n_paths = from.num_unique_paths_to(&to);
            assert_eq!(n_paths, expected, "failed from {:?} to {:?}", from, to);
        }
    }
}
