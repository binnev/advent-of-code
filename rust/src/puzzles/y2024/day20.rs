use std::collections::{HashMap, HashSet};

use crate::utils::{Coord, SparseMatrix};

pub fn part1(input: &str) -> usize {
    let map: SparseMatrix<char> = input.into();
    let end = map.locate('E').unwrap();
    let distances_to_end =
        dijkstra(end, &map, get_neighbours_and_movement_cost);
    let cheats = find_cheats(&distances_to_end, 2);
    cheats
        .iter()
        .filter(|cheat| cheat.score >= 100)
        .count()
}
pub fn part2(input: &str) -> usize {
    let map: SparseMatrix<char> = input.into();
    let end = map.locate('E').unwrap();
    let distances_to_end =
        dijkstra(end, &map, get_neighbours_and_movement_cost);
    let cheats = find_cheats(&distances_to_end, 20);
    cheats
        .iter()
        .filter(|cheat| cheat.score >= 100)
        .count()
}

/// Find all the possible "cheats": (start, end, picoseconds saved).
/// For every empty square in the maze, consider every other empty square in the
/// maze. Criteria for a valid cheat:
/// 1. We can get from A to B faster by cheating than by following the path
/// 2. The end square is closer to the maze finish than the start square
fn find_cheats(
    distances_to_end: &HashMap<Coord, usize>,
    max_cheat_distance: usize,
) -> Vec<Cheat> {
    let mut cheats = vec![];
    for (from, from_dist) in distances_to_end.iter() {
        for (to, to_dist) in distances_to_end.iter() {
            // Only consider cheats that bring us _closer_ to the finish -- i.e.
            // where from_dist > to_dist
            if from_dist > to_dist {
                let path_distance = from_dist.abs_diff(*to_dist);
                let cheat_distance = from.taxicab_dist_to(&to) as usize;
                if path_distance > cheat_distance
                    && cheat_distance <= max_cheat_distance
                {
                    cheats.push(Cheat {
                        from:  *from,
                        to:    *to,
                        score: path_distance - cheat_distance,
                    });
                }
            }
        }
    }
    cheats
}
#[derive(PartialEq, Eq, Hash, Debug)]
struct Cheat {
    from:  Coord,
    to:    Coord,
    score: usize, // number of steps saved by taking the cheat
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
        .filter(|neighbour| is_empty(*neighbour, map))
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
    fn test_find_cheats_simple() {
        let my_example = "###
...
A#B
S#E";
        let map: SparseMatrix<char> = my_example.into();
        let end = map.locate('E').unwrap();
        let distances_to_end =
            dijkstra(end, &map, get_neighbours_and_movement_cost);
        let cheats: HashSet<_> = find_cheats(&distances_to_end, 10)
            .into_iter()
            .collect();
        assert_eq!(cheats.len(), 4);
        for expected in [
            Cheat {
                from:  Coord(0, 3),
                to:    Coord(2, 3),
                score: 4,
            },
            Cheat {
                from:  Coord(0, 3),
                to:    Coord(2, 2),
                score: 2,
            },
            Cheat {
                from:  Coord(0, 2),
                to:    Coord(2, 3),
                score: 2,
            },
            Cheat {
                from:  Coord(0, 2),
                to:    Coord(2, 2),
                score: 2,
            },
        ] {
            assert!(
                cheats.contains(&expected),
                "Couldn't find {expected:?}. All cheats: {cheats:?}"
            );
        }
    }
    #[test]
    fn test_find_cheats() {
        // ------------------------------------------------------------------
        let map: SparseMatrix<char> = EXAMPLE.into();
        let end = map.locate('E').unwrap();
        let distances_to_end =
            dijkstra(end, &map, get_neighbours_and_movement_cost);

        // Part 1: cheat distance = 2
        let cheats = find_cheats(&distances_to_end, 2);
        let mut savings = HashMap::new();
        for cheat in cheats {
            savings
                .entry(cheat.score)
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
        let cheats = find_cheats(&distances_to_end, 20);
        let mut savings = HashMap::new();
        for cheat in cheats {
            savings
                .entry(cheat.score)
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
}
pub const EXAMPLE: &str = "###############
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
const WALL: char = '#';
