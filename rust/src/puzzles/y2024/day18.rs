use crate::utils::{Coord, SparseMatrix};
use std::collections::{HashMap, HashSet};

pub fn part1(input: &str) -> usize {
    find_shortest_distance(input, 70, 1024)
}
pub fn part2(input: &str) -> String {
    let blocking_coord = find_first_blocking_byte(input, 70, 1024);
    format!("{},{}", blocking_coord.0, blocking_coord.1)
}
/// TODO: Optimisation: find all the possible paths once, and then find the
/// first byte that blocks all of them
fn find_first_blocking_byte(
    input: &str,
    grid_size: i64,
    non_blocking_bytes: usize, /* the number of bytes we know won't block
                                * the way */
) -> Coord {
    let unsafe_bytes = parse(input);
    let mut map = make_matrix(grid_size + 1);
    let start = Coord(0, 0);
    let end = Coord(grid_size, grid_size);
    for (ii, coord) in unsafe_bytes.into_iter().enumerate() {
        map.insert(coord, CORRUPTED);
        // don't bother finding paths for bytes we know to be non-blocking.
        if ii < non_blocking_bytes {
            continue;
        }
        let distances = dijkstra(start, &map);
        if distances.get(&end).is_none() {
            return coord;
        }
    }
    unreachable!()
}
/// Construct the maze and find the shortest distance from start to finish
fn find_shortest_distance(
    input: &str,
    grid_size: i64,
    n_bytes: usize,
) -> usize {
    let unsafe_bytes = parse(input);
    let mut map = make_matrix(grid_size + 1);
    for idx in 0..n_bytes {
        let coord = match unsafe_bytes.get(idx) {
            Some(coord) => coord.clone(),
            None => break,
        };
        map.insert(coord, CORRUPTED);
    }
    let start = Coord(0, 0);
    let end = Coord(grid_size, grid_size);
    let distances = dijkstra(start, &map);
    distances
        .get(&end)
        .expect("No path from start to end!")
        .clone()
}
/// Calculate the min distance from the start square to every other square
fn dijkstra(start: Coord, map: &SparseMatrix<char>) -> HashMap<Coord, usize> {
    // Keep track of the shortest distance to each coord here
    let mut shortest_distances: HashMap<Coord, usize> =
        HashMap::from([(start, 0)]);
    // This stores the active "leading edge" of the BFS
    let mut frontier: HashSet<Coord> = HashSet::from([start]);
    // Since the cost of visiting neighbours is uniform, we can use a simple
    // step counter
    let mut distance = 0;
    loop {
        distance += 1;
        let mut safe_neighbours = HashSet::new();
        for coord in frontier {
            for neighbour in coord.neighbours() {
                // limit to map. Avoid unsafe coords.
                match map.get(&neighbour) {
                    Some(&SAFE) => {
                        safe_neighbours.insert(neighbour);
                    }
                    _ => continue, // out of bounds or unsafe
                }
            }
        }
        let mut new_frontier = HashSet::new();
        for neighbour in safe_neighbours {
            match shortest_distances.get(&neighbour) {
                // If we've already recorded a shorter distance, do nothing.
                Some(&shortest_distance) if shortest_distance < distance => {}
                // If we haven't visited this coord yet, or if the current
                // distance is better than the previous recorded distance,
                // keep exploring and update the best distance.
                _ => {
                    new_frontier.insert(neighbour);
                    shortest_distances.insert(neighbour, distance);
                }
            }
        }
        if new_frontier.len() == 0 {
            break;
        }
        frontier = new_frontier;
    }
    shortest_distances
}
fn make_matrix(size: i64) -> SparseMatrix<char> {
    let mut matrix = SparseMatrix::new();
    for x in 0..size {
        for y in 0..size {
            let coord = (x, y).into();
            matrix.insert(coord, SAFE);
        }
    }
    matrix
}
fn parse(input: &str) -> Vec<Coord> {
    input
        .trim()
        .lines()
        .map(|line| {
            let parts: Vec<&str> = line.split(",").take(2).collect();
            let x = parts[0].parse().unwrap();
            let y = parts[1].parse().unwrap();
            Coord(x, y)
        })
        .collect()
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_part1() {
        assert_eq!(find_shortest_distance(EXAMPLE, 6, 12), 22);
    }
    #[test]
    fn test_part2() {
        assert_eq!(find_first_blocking_byte(EXAMPLE, 6, 12), Coord(6, 1));
    }
}
pub const EXAMPLE: &str = "5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0";
const SAFE: char = '.';
const CORRUPTED: char = '#';
