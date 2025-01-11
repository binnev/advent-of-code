use std::collections::HashSet;

use crate::utils::{coord_neighbours, Coord, SparseMatrix};

pub fn part1(input: &str) -> usize {
    let map: SparseMatrix<char> = input.into();
    let mut explored: HashSet<Coord> = HashSet::new();
    let mut out = 0;
    for (coord, _) in map.iter() {
        if explored.contains(coord) {
            continue;
        }
        let (region, perimeter) = explore_region(coord, &map);
        explored.extend(&region);
        out += region.len() * perimeter;
    }
    out
}
pub fn part2(input: &str) -> usize {
    0
}

const EXAMPLE1: &str = "AAAA
BBCD
BBCC
EEEC";
const EXAMPLE2: &str = "RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE";

/// Explore the region belonging to the starting coord.
fn explore_region(
    start: &Coord,
    map: &SparseMatrix<char>,
) -> (HashSet<Coord>, usize) {
    let region_colour = map.get(&start).unwrap();
    let mut perimeter = 0;
    let mut region: HashSet<Coord> = HashSet::from([start.clone()]);
    let mut frontier = region.clone();
    loop {
        let mut neighbours = HashSet::new();
        for coord in frontier {
            for neighbour in coord_neighbours(&coord) {
                if region.contains(&neighbour) {
                    continue;
                }
                if map.get(&neighbour) == Some(region_colour) {
                    // Same colour as this region
                    neighbours.insert(neighbour);
                } else {
                    // Other colour, or coord not in map
                    perimeter += 1;
                }
            }
        }
        if neighbours.len() == 0 {
            break;
        }
        region.extend(&neighbours);
        frontier = neighbours;
    }
    (region, perimeter)
}

mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE1), 140);
        assert_eq!(part1(EXAMPLE2), 1930);
    }
    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE2), 0);
    }
}
