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
    let cheats = find_cheats(&map, &distances_to_end, 2);
    cheats
        .iter()
        .filter(|(_, _, score)| score >= &100)
        .count()
}
pub fn part2(input: &str) -> usize {
    let map: SparseMatrix<char> = input.into();
    let start = map.locate('S').unwrap();
    let end = map.locate('E').unwrap();
    let distances_to_end =
        dijkstra(end, &map, get_neighbours_and_movement_cost);
    let cheats = find_cheats(&map, &distances_to_end, 20);
    cheats
        .iter()
        .filter(|(_, _, score)| score >= &100)
        .count()
}

// Find all the possible "cheats": (start, end, picoseconds saved).
fn find_cheats(
    map: &SparseMatrix<char>,
    distances_to_end: &HashMap<Coord, usize>,
    cheat_distance: usize,
) -> Vec<(Coord, Coord, usize)> {
    let mut cheats = vec![];
    for (&from, current_distance) in distances_to_end {
        for to in get_cheat_squares(from, map, cheat_distance) {
            let cheat_distance = distances_to_end
                .get(&to)
                .expect(&format!("Couldn't find distance for {to:?}"));
            if current_distance > cheat_distance {
                let score = get_cheat_score(from, to, distances_to_end);
                cheats.push((from, to, score));
            }
        }
    }
    cheats
}
/// Do a mini BFS outwards from the `from` square, up to the max allowable
/// distance
/// .................
/// ........3........
/// .......323.......
/// ......32123......
/// .....321F123.....
/// ......32123......
/// .......323.......
/// ........3........
/// .................
fn get_cheat_squares(
    from: Coord,
    map: &SparseMatrix<char>,
    max_distance: usize,
) -> HashSet<Coord> {
    // Do a mini BFS to
    // 1. find all nearby squares within `max_distance`
    // 2. find all reachable squares within `max_distance`
    let mut nearby = HashSet::from([from]); // all squares within `max_distance`
    let mut reachable = HashSet::from([from]); // _reachable_ squares within `max_distance`
    let mut nearby_frontier = nearby.clone();
    let mut reachable_frontier = reachable.clone();
    let mut dist = 1;
    while dist <= max_distance {
        let mut nearby_neighbours = HashSet::new();
        for coord in nearby_frontier {
            nearby_neighbours.extend(coord.neighbours());
        }
        nearby_frontier = nearby_neighbours;
        nearby.extend(&nearby_frontier);

        let mut reachable_neighbours = HashSet::new();
        for coord in reachable_frontier {
            reachable_neighbours.extend(get_empty_neighbours(coord, map));
        }
        reachable_frontier = reachable_neighbours;
        reachable.extend(&reachable_frontier);
        dist += 1;
    }

    nearby
        .into_iter()
        // Filter for empty squares that are in the map
        .filter(|coord| is_empty(*coord, map))
        // Filter out reachable coords because they are not cheats.
        .filter(|coord| !reachable.contains(coord))
        .collect()
}
/// Return true if the coord is in the map and the value is not a wall
fn is_empty(coord: Coord, map: &SparseMatrix<char>) -> bool {
    match map.get(&coord) {
        Some(value) if value != &WALL => true,
        _ => false,
    }
}
fn get_empty_neighbours(node: Coord, map: &SparseMatrix<char>) -> Vec<Coord> {
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
    get_empty_neighbours(node, map)
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
    let dist = from.taxicab_dist_to(&to) as usize;
    distances_to_end.get(&from).unwrap()
        - distances_to_end.get(&to).unwrap()
        - dist // because we spend movement going through the wall
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

        // Part 1: cheat distance = 2
        let cheats = find_cheats(&map, &distances_to_end, 2);
        let mut savings = HashMap::new();
        for (_, _, score) in cheats {
            savings
                .entry(score)
                .and_modify(|e| *e += 1)
                .or_insert(1);
        }
        assert_eq!(savings[&2], 14); // There are 14 cheats that save 2 picoseconds.
        assert_eq!(savings[&4], 14); // There are 14 cheats that save 4 picoseconds.
        assert_eq!(savings[&6], 2); // There are 2 cheats that save 6 picoseconds.
        assert_eq!(savings[&8], 4); // There are 4 cheats that save 8 picoseconds.
        assert_eq!(savings[&10], 2); // There are 2 cheats that save 10 picoseconds.
        assert_eq!(savings[&12], 3); // There are 3 cheats that save 12 picoseconds.
        assert_eq!(savings[&20], 1); // There is one cheat that saves 20 picoseconds.
        assert_eq!(savings[&36], 1); // There is one cheat that saves 36 picoseconds.
        assert_eq!(savings[&38], 1); // There is one cheat that saves 38 picoseconds.
        assert_eq!(savings[&40], 1); // There is one cheat that saves 40 picoseconds.
        assert_eq!(savings[&64], 1); // There is one cheat that saves 64 picoseconds.

        // Part 2: cheat distance = 20
        let cheats = find_cheats(&map, &distances_to_end, 20);
        let mut savings = HashMap::new();
        for (_, _, score) in cheats {
            savings
                .entry(score)
                .and_modify(|e| *e += 1)
                .or_insert(1);
        }
        assert_eq!(savings[&50], 32); // There are 32 cheats that save 50 picoseconds.
        assert_eq!(savings[&52], 31); // There are 31 cheats that save 52 picoseconds.
        assert_eq!(savings[&54], 29); // There are 29 cheats that save 54 picoseconds.
        assert_eq!(savings[&56], 39); // There are 39 cheats that save 56 picoseconds.
        assert_eq!(savings[&58], 25); // There are 25 cheats that save 58 picoseconds.
        assert_eq!(savings[&60], 23); // There are 23 cheats that save 60 picoseconds.
        assert_eq!(savings[&62], 20); // There are 20 cheats that save 62 picoseconds.
        assert_eq!(savings[&64], 19); // There are 19 cheats that save 64 picoseconds.
        assert_eq!(savings[&66], 12); // There are 12 cheats that save 66 picoseconds.
        assert_eq!(savings[&68], 14); // There are 14 cheats that save 68 picoseconds.
        assert_eq!(savings[&70], 12); // There are 12 cheats that save 70 picoseconds.
        assert_eq!(savings[&72], 22); // There are 22 cheats that save 72 picoseconds.
        assert_eq!(savings[&74], 4); // There are 4 cheats that save 74 picoseconds.
        assert_eq!(savings[&76], 3); // There are 3 cheats that save 76 picoseconds.

        ()
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
