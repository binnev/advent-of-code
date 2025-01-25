use std::{
    collections::{HashMap, HashSet},
    iter::repeat,
};

use regex::bytes;

use crate::utils::{Coord, SparseMatrix};

pub fn part1(input: &str) -> usize {
    do_the_thing(input, 70, 1024)
}
pub fn part2(input: &str) -> usize {
    0
}
/// Construct the maze and find the shortest distance from start to finish
fn do_the_thing(input: &str, grid_size: i64, n_bytes: usize) -> usize {
    let unsafe_bytes = parse(input);
    let mut map = make_matrix(grid_size + 1);
    drop_bytes(unsafe_bytes, &mut map, n_bytes);
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
        // {
        //     let mut printable = SparseMatrix {
        //         contents: map.contents.clone(),
        //     };
        //     printable.insert_many(new_frontier.clone(), 'O');
        //     println!("\n{printable}");
        // }
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
            let mut parts: Vec<&str> = line.split(",").take(2).collect();
            let x = parts[0].parse().unwrap();
            let y = parts[1].parse().unwrap();
            Coord(x, y)
        })
        .collect()
}
/// Simulate the bytes falling at the given coordinates to build the maze
fn drop_bytes(
    unsafe_bytes: Vec<Coord>,
    map: &mut SparseMatrix<char>,
    n: usize, // number of bytes to simulate
) -> Option<()> {
    for idx in 0..n {
        let coord = unsafe_bytes.get(idx)?.clone();
        map.insert(coord, CORRUPTED);
    }
    Some(())
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_part1() {
        assert_eq!(do_the_thing(EXAMPLE, 6, 12), 22);
    }
    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 0);
    }
}
const EXAMPLE: &str = "5,4
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
