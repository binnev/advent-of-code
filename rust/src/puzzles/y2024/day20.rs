use std::collections::{HashMap, HashSet};

use crate::utils::{Coord, Direction::*, SparseMatrix};

/// Here's the plan:
/// 1. Dijkstra from E -> S so that we know the distance from every square to
///    the finish.
/// 2. Go along the only path, and scan a 4x4 grid around for "cheats". The time
///    saved by each cheat will be the current square's distance to E minus the
///    target cheat square's distance to E.
pub fn part1(input: &str) -> usize {
    let map: SparseMatrix<char> = input.into();
    let start = map.locate('S').unwrap();
    let end = map.locate('E').unwrap();
    let distances_to_end =
        dijkstra(end, &map, get_neighbours_and_movement_cost);
    let cheats = find_cheats(&map, &distances_to_end);
    cheats
        .iter()
        .filter(|(_, _, picoseconds_saved)| picoseconds_saved >= &100)
        .count()
}
pub fn part2(input: &str) -> usize {
    0
}

// Find all the possible "cheats": (start, end, picoseconds saved).
fn find_cheats(
    map: &SparseMatrix<char>,
    distances_to_end: &HashMap<Coord, usize>,
) -> Vec<(Coord, Coord, usize)> {
    let mut cheats = vec![];
    for (&from, current_distance) in distances_to_end {
        for to in get_cheat_squares(from, map) {
            let cheat_distance = distances_to_end.get(&to).unwrap();
            if current_distance > cheat_distance {
                let score = get_cheat_score(from, to, distances_to_end);
                cheats.push((from, to, score));
            }
        }
    }
    cheats
}
/// These are the cheat squares available from H:
/// ...C...
/// ...#...
/// .C#H#C.
/// ...#...
/// ...C...
fn get_cheat_squares(from: Coord, map: &SparseMatrix<char>) -> Vec<Coord> {
    let mut cheats = vec![];
    for (first, second) in [
        (from.north(), from.north().north()),
        (from.east(), from.east().east()),
        (from.south(), from.south().south()),
        (from.west(), from.west().west()),
    ] {
        if !is_empty(first, map) && is_empty(second, map) {
            cheats.push(second);
        }
    }
    cheats
}
fn is_empty(coord: Coord, map: &SparseMatrix<char>) -> bool {
    match map.get(&coord) {
        Some(value) if value != &WALL => true,
        _ => false,
    }
}
fn get_neighbours(node: Coord, map: &SparseMatrix<char>) -> Vec<Coord> {
    node.neighbours()
        .into_iter()
        .filter(|neighbour| match map.get(neighbour) {
            Some(value) if value != &WALL => true,
            _ => false,
        })
        .collect()
}
fn get_neighbours_and_movement_cost(
    node: Coord,
    map: &SparseMatrix<char>,
) -> Vec<(Coord, usize)> {
    let movement_cost = 1;
    get_neighbours(node, map)
        .into_iter()
        .map(|neighbour| (neighbour, movement_cost))
        .collect()
}
/// Calculate the distance saved by taking the cheat. Bear in mind that
/// distances are from the _end_ square.
fn get_cheat_score(
    from: Coord,
    to: Coord,
    distances_to_end: &HashMap<Coord, usize>,
) -> usize {
    distances_to_end.get(&from).unwrap()
        - distances_to_end.get(&to).unwrap()
        - 2 // because we spend 2 moving through the wall
}
/// Generic Dijkstra implementation to find the distance from the start to every
/// reachable square in the map
fn dijkstra(
    start: &Coord,
    map: &SparseMatrix<char>,
    neighbours_func: fn(
        node: Coord,
        map: &SparseMatrix<char>,
    ) -> Vec<(Coord, usize)>, // neighbour coord + movement cost to get there
) -> HashMap<Coord, usize> {
    let mut distances: HashMap<Coord, usize> =
        HashMap::from([(start.clone(), 0)]);
    let mut frontier: HashSet<Coord> = HashSet::from([start.clone()]);
    while frontier.len() > 0 {
        let mut new_frontier = HashSet::new();
        for node in frontier {
            let current_distance = distances
                .get(&node)
                .unwrap_or(&0)
                .clone();
            for (neighbour, movement_cost) in neighbours_func(node, map) {
                let neighbour_distance = current_distance + movement_cost;
                match distances.get(&neighbour) {
                    // If we have already recorded a distance to the
                    // neighbouring square that is better than what we just
                    // found, ignore the new finding and do nothing.
                    Some(best_distance)
                        if best_distance <= &neighbour_distance => {}
                    // If we have no recorded distance, or if the existing
                    // distance is worse than the new one, insert the new
                    // distance and keep investigating the neighbour node.
                    _ => {
                        distances.insert(neighbour, neighbour_distance);
                        new_frontier.insert(neighbour);
                    }
                }
            }
        }
        frontier = new_frontier;
    }
    distances
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 0);
    }
    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 0);
    }

    #[test]
    fn test_dijkstra() {
        let map: SparseMatrix<char> = EXAMPLE.into();
        let start = map.locate('S').unwrap();
        let end = map.locate('E').unwrap();
        let distances_to_end =
            dijkstra(end, &map, get_neighbours_and_movement_cost);
        assert_eq!(distances_to_end.get(start).unwrap(), &84);
    }
    #[test]
    fn test_find_cheats() {
        let map: SparseMatrix<char> = EXAMPLE.into();
        let end = map.locate('E').unwrap();
        let distances_to_end =
            dijkstra(end, &map, get_neighbours_and_movement_cost);
        let cheats = find_cheats(&map, &distances_to_end);
        let mut n_cheats_per_saving = HashMap::new();
        for (_, _, score) in cheats {
            n_cheats_per_saving
                .entry(score)
                .and_modify(|e| *e += 1)
                .or_insert(1);
        }
        let expected = HashMap::from([
            (2, 14), // There are 14 cheats that save 2 picoseconds.
            (4, 14), // There are 14 cheats that save 4 picoseconds.
            (6, 2),  // There are 2 cheats that save 6 picoseconds.
            (8, 4),  // There are 4 cheats that save 8 picoseconds.
            (10, 2), // There are 2 cheats that save 10 picoseconds.
            (12, 3), // There are 3 cheats that save 12 picoseconds.
            (20, 1), // There is one cheat that saves 20 picoseconds.
            (36, 1), // There is one cheat that saves 36 picoseconds.
            (38, 1), // There is one cheat that saves 38 picoseconds.
            (40, 1), // There is one cheat that saves 40 picoseconds.
            (64, 1), // There is one cheat that saves 64 picoseconds.
        ]);
        assert_eq!(n_cheats_per_saving, expected);
    }

    #[test]
    fn test_get_cheat_score() {
        let map: SparseMatrix<char> = EXAMPLE.into();
        let end = map.locate('E').unwrap();
        let distances_to_end =
            dijkstra(end, &map, get_neighbours_and_movement_cost);
        for (from, to, expected) in [
            (Coord(7, 1), Coord(9, 1), 12),
            (Coord(9, 7), Coord(11, 7), 20),
            (Coord(8, 7), Coord(8, 9), 38),
            (Coord(7, 7), Coord(5, 7), 64),
        ] {
            let result = get_cheat_score(from, to, &distances_to_end);
            assert_eq!(result, expected);
        }
    }
}
const EXAMPLE: &str = "###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############";
const EMPTY: char = '.';
const WALL: char = '#';
