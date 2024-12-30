use itertools::Itertools;
use std::collections::{HashMap, HashSet};

use crate::utils::{Coord, SparseMatrix};

pub fn part1(input: &str) -> String {
    let grid: SparseMatrix = input.into();
    let antennae = aggregate_antennae(&grid);
    let mut antinodes = HashSet::new();
    for (_, coords) in antennae.iter() {
        for combo in coords.iter().combinations(2) {
            for node in calculate_antinodes_part1(combo[0], combo[1]) {
                if grid.contains_key(&node) {
                    antinodes.insert(node);
                }
            }
        }
    }
    format!("{}", antinodes.len())
}
pub fn part2(input: &str) -> String {
    let grid: SparseMatrix = input.into();
    let antennae = aggregate_antennae(&grid);
    let mut antinodes = HashSet::new();
    for (_, coords) in antennae.iter() {
        for combo in coords.iter().combinations(2) {
            for node in calc_antinodes_part2(combo[0], combo[1], &grid) {
                antinodes.insert(node);
            }
        }
    }
    format!("{}", antinodes.len())
}

/// I'd like to iterate over the input matrix just once.
/// Maybe we can reverse it, to produce
/// {
///     A: [(x,y), (x,y)],
///     a: [(x,y), ...],
///     0: [...],
/// }
/// so that we can look up quickly on antenna name. Then for each list of coords
/// associated with an antenna name, we can go through all the pairs, calculate
/// the antinode locations (checking that they're inside the grid) and add them
/// to a hashset.
fn aggregate_antennae(grid: &SparseMatrix) -> HashMap<char, Vec<Coord>> {
    let mut antennae: HashMap<char, Vec<Coord>> = HashMap::new();
    for (&coord, &ch) in grid.iter() {
        if ch != '.' {
            antennae
                .entry(ch)
                .and_modify(|e| e.push(coord))
                .or_insert(vec![coord]);
        }
    }
    antennae
}
/// "...an antinode occurs at any point that is perfectly in line with two
/// antennas of the same frequency - but only when one of the antennas is twice
/// as far away as the other. This means that for any pair of antennas with the
/// same frequency, there are two antinodes, one on either side of them."
fn calculate_antinodes_part1(a: &Coord, b: &Coord) -> Vec<Coord> {
    let (x1, y1) = a;
    let (x2, y2) = b;
    let dx = x2 - x1;
    let dy = y2 - y1;
    let left = (x1 - dx, y1 - dy);
    let right = (x2 + dx, y2 + dy);
    vec![left, right]
}
/// "After updating your model, it turns out that an antinode occurs at any grid
/// position exactly in line with at least two antennas of the same frequency,
/// regardless of distance. This means that some of the new antinodes will occur
/// at the position of each antenna (unless that antenna is the only one of its
/// frequency)."
fn calc_antinodes_part2(
    a: &Coord,
    b: &Coord,
    grid: &SparseMatrix,
) -> Vec<Coord> {
    let mut out = vec![*a, *b]; // the antennae are always antinodes now?
    let (x1, y1) = a;
    let (x2, y2) = b;
    let dx = x2 - x1;
    let dy = y2 - y1;
    // get right nodes that are in the grid
    for ii in 1.. {
        let node = (x2 + dx * ii, y2 + dy * ii);
        if !grid.contains_key(&node) {
            break;
        }
        out.push(node);
    }
    // left nodes
    for ii in 1.. {
        let node = (x1 - dx * ii, y1 - dy * ii);
        if !grid.contains_key(&node) {
            break;
        }
        out.push(node);
    }
    out
}
const EXAMPLE: &str = "............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............";

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), "14");
    }
    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), "34");
    }
}
