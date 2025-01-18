use std::collections::HashSet;

use crate::utils::{coord_neighbours, Coord, SparseMatrix};

/// Find all the "hiking trails" for each "trailhead".
/// "Hiking trail" = path from 0 to 9
/// "trailhead" = 0
///
/// The number of 9s accessible from each trailhead is the trailhead's score.
/// Sum the scores of all the trailheads to get the answer.
///
/// Optimisation: build a directed graph so that we don't have to retrace every
/// hiking trail from every trailhead (trails will likely merge)
///
/// We could even BFS out from the 9s; for each coord, count the number of 9s
/// that are accessible from it. Then when we've worked our way all the way back
/// to the trailheads, they'll have their scores.
///
/// Or reverse it: BFS out from the trailheads. That way inaccessible 9s won't
/// get searched. And the frontiers from different trailheads will merge so we
/// won't redo work. We'll iterate over the map exactly once. We'll need to keep
/// track of how many 9s are accessible for each frontier. And handle merging
/// logic
///
/// This map has the following routes:
/// 0123  0┬┬╮
/// 1234  ╰┴┴┤
/// 8765  ╭┬┬┤
/// 9876  9┴┴╯
///
/// Box-drawing chars:
/// ╭─┬╮
/// │ ││
/// ├─┼┤
/// ╰─┴╯
///
/// This map:         
/// 10..9..  ╭0..9..
/// 2...8..  │...│..
/// 3...7..  │...│..
/// 4567654  ╰──┬┴─╮
/// ...8..3  ...│..│
/// ...9..2  ...9..│
/// .....01  .....0╯
///
/// Now let's use numbers to represent how many 9s are reachable from each
/// square. BFS from each trailhead and then add the scores:
///
/// 11.....   ....X..   11..X..  
/// 1......   ....1..   1...1..  
/// 1......   ....1..   1...1..  
/// 1111111 + ....111 = 1111222  
/// ...1..1   ......1   ...1..2  
/// ...X..1   ......1   ...X..2  
/// .....11   .....11   .....22  
///
/// We can optimise this: the second scan could stop when it hits the midline;
/// the path downwards from that square is already known:
///
/// ....X..
/// ....1..
/// ....1..
/// ....1..
/// .......
/// .......
/// .......

pub fn part1(input: &str) -> usize {
    let map = parse(input);
    let summits: HashSet<Coord> = map
        .iter()
        .filter(|(_, height)| **height == SUMMIT)
        .map(|(coord, _)| coord.clone())
        .collect();
    let trailheads: HashSet<Coord> = map
        .iter()
        .filter(|(_, height)| **height == TRAILHEAD)
        .map(|(coord, _)| coord.clone())
        .collect();
    let mut scores: SparseMatrix<usize> = SparseMatrix::new();
    for summit in summits {
        let visited = bfs_down(&summit, &map);
        for coord in visited {
            scores
                .entry(coord)
                .and_modify(|e| *e += 1)
                .or_insert(1);
        }
    }
    trailheads
        .iter()
        .map(|coord| scores.get(coord).unwrap_or(&0))
        .sum()
}
pub fn part2(input: &str) -> usize {
    let map = parse(input);
    let trailheads: HashSet<Coord> = map
        .iter()
        .filter(|(_, height)| **height == TRAILHEAD)
        .map(|(coord, _)| coord.clone())
        .collect();
    let mut out = 0;
    for trailhead in trailheads {
        out += bfs_up(&trailhead, &map);
    }
    out
}

/// BFS up from a trailhead and return the number of possible paths that lead to
/// summits
fn bfs_up(start: &Coord, map: &SparseMatrix<u8>) -> usize {
    let mut frontier = vec![start.clone()];
    let mut summit_count = 0;
    loop {
        // Count the summits in the frontier and add them to the total score
        let new_summits = frontier
            .iter()
            .filter(|coord| map.get(coord) == Some(&SUMMIT))
            .count();
        summit_count += new_summits;

        // get neighbours of all frontier nodes. IMPORTANT: don't de-dupe. The
        // duplication is what allows us to find _all_ the possible paths.
        let mut neighbours = vec![];
        for coord in frontier.iter() {
            neighbours.extend(uphill_neighbours(&coord, map));
        }

        if neighbours.len() == 0 {
            break;
        }

        frontier = neighbours.into_iter().collect();
    }
    summit_count
}

/// BFS downwards from a summit, and return the set of unique coords that are
/// reachable from this summit.
fn bfs_down(start: &Coord, map: &SparseMatrix<u8>) -> HashSet<Coord> {
    let mut visited = HashSet::from([start.clone()]);
    let mut frontier = visited.clone();
    loop {
        // Get unique neighbours of the frontier nodes
        // That means ignore ones already visited
        let mut neighbours = HashSet::new();
        for coord in frontier {
            neighbours.extend(downhill_neighbours(&coord, &map));
        }

        // If there are no unvisited neighbours, break.
        if neighbours.len() == 0 {
            break;
        }

        visited.extend(&neighbours);
        frontier = neighbours;
    }
    visited
}
/// Get the downhill neighbours of a coord
fn downhill_neighbours(coord: &Coord, map: &SparseMatrix<u8>) -> Vec<Coord> {
    coord_neighbours(coord)
        .into_iter()
        // If is_downhill returns None it's because the neighbour is not in the
        // map. In that case we should not return that neighbour.
        .filter(|neighbour| {
            is_1_downhill(coord, neighbour, map).unwrap_or(false)
        })
        .collect()
}
/// Get the uphill neighbours of a coord
fn uphill_neighbours(coord: &Coord, map: &SparseMatrix<u8>) -> Vec<Coord> {
    coord_neighbours(coord)
        .into_iter()
        .filter(|neighbour| is_1_uphill(coord, neighbour, map).unwrap_or(false))
        .collect()
}
// Check if the second coord is exactly 1 step lower than the first coord.
// Return None if either coord is not in the map
fn is_1_downhill(
    from: &Coord,
    to: &Coord,
    map: &SparseMatrix<u8>,
) -> Option<bool> {
    map.get(&from)
        .zip(map.get(&to))
        .map(|(from_height, to_height)| {
            to_height < from_height && to_height.abs_diff(*from_height) == 1
        })
}
fn is_1_uphill(
    from: &Coord,
    to: &Coord,
    map: &SparseMatrix<u8>,
) -> Option<bool> {
    map.get(&from)
        .zip(map.get(&to))
        .map(|(from_height, to_height)| {
            to_height > from_height && to_height.abs_diff(*from_height) == 1
        })
}
fn parse(input: &str) -> SparseMatrix<u8> {
    let chars: SparseMatrix<char> = input.into();
    SparseMatrix {
        contents: chars
            .contents
            .into_iter()
            // Ignore '.' values
            .filter_map(|(coord, ch)| {
                ch.to_digit(10)
                    .map(|digit| (coord, digit as u8))
            })
            .collect(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE2), 3);
        assert_eq!(part1(EXAMPLE3), 2);
        assert_eq!(part1(EXAMPLE4), 1);
        assert_eq!(part1(EXAMPLE5), 4);
        assert_eq!(part1(EXAMPLE), 36);
    }
    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE6), 3);
        assert_eq!(part2(EXAMPLE5), 13);
        assert_eq!(part2(EXAMPLE7), 227);
        assert_eq!(part2(EXAMPLE), 81);
    }
}
const EXAMPLE: &str = "89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732";
const EXAMPLE2: &str = "10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01";
const EXAMPLE3: &str = "...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9";
const EXAMPLE4: &str = "0123
1234
8765
9876";
const EXAMPLE5: &str = "..90..9
...1.98
...2..7
6543456
765.987
876....
987....";
const EXAMPLE6: &str = ".....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....";
const EXAMPLE7: &str = "012345
123456
234567
345678
4.6789
56789.";
const TRAILHEAD: u8 = 0;
const SUMMIT: u8 = 9;
