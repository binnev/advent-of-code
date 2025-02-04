use crate::utils::{Coord, SparseMatrix};
use std::collections::HashSet;

/// Find the number of fence parts required to fence in areas with the same
/// letter:
///
/// +-+-+-+-+
/// |A A A A|
/// +-+-+-+-+     +-+
///               |D|
/// +-+-+   +-+   +-+
/// |B B|   |C|
/// + - +   + +-+
/// |B B|   |C C|
/// +-+-+   +-+ +
///           |C|
/// +-+-+-+   +-+
/// |E E E|
/// +-+-+-+
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

/// Now instead of the number of fence parts, we want to find the number of
/// _sides_ -- i.e. each straight section of fence.
///
/// Bear in mind that just finding and following the outer perimiter won't find
/// internal holes in the area.
pub fn part2(input: &str) -> usize {
    let map: SparseMatrix<char> = input.into();
    let mut explored: HashSet<Coord> = HashSet::new();
    let mut out = 0;
    for coord in map.keys() {
        if explored.contains(coord) {
            continue;
        }
        let (region, _) = explore_region(coord, &map);
        explored.extend(&region);
        let edges = count_edges(&region);
        out += region.len() * edges;
    }
    out
}

/// Consider the following shape. It has 4 horizontal edges:
///  -1--       
/// |XXXX|   
/// |XXXX -2-
/// |XXXXXXXX|
/// |XXXXXXXX|
///  -3- XXXX|
///     |XXXX|
///      -4--
/// Scan through it 2 rows at a time. Any current[x] != previous[x] -> edge
///             previous    edge
/// ........
/// XXXX....    ........    XXXX....  
/// XXXX....    XXXX....    ........
/// XXXXXXXX    XXXX....    ....XXXX
/// XXXXXXXX    XXXXXXXX    ........
/// ....XXXX    XXXXXXXX    XXXX....
/// ....XXXX    ....XXXX    ........
/// ........    ....XXXX    ....XXXX    
///
/// Important case: 2 edges next to each other that are not the same edge. This
/// requires us to differentiate between start/end edges.
///         previous    edge
/// -1-                      
/// XXX     ......      SSS...
/// XXX     XXX...      ......
/// XXX-3-  XXX...      ......
/// -2-XXX  XXX...      EEESSS
///    XXX  ...XXX      ......
///    XXX  ...XXX      ......
///    -4-  ...XXX      ...EEE
fn count_edges(region: &HashSet<Coord>) -> usize {
    let mut num_edges = 0;
    let ((xmin, xmax), (ymin, ymax)) = get_limits(region);

    // Scan rows for H edges
    for y in ymin..ymax + 2 {
        let mut previous = None;
        for x in xmin..xmax + 2 {
            let top = (x, y - 1);
            let bottom = (x, y);
            let current = match (
                region.contains(&top.into()),
                region.contains(&bottom.into()),
            ) {
                (false, true) => Some(Edge::Start),
                (true, false) => Some(Edge::End),
                _ => None,
            };
            if previous != current && previous.is_some() {
                num_edges += 1
            }
            previous = current;
        }
    }

    // Scan columns for V edges
    for x in xmin..xmax + 2 {
        let mut previous = None;
        for y in ymin..ymax + 2 {
            let left = (x - 1, y);
            let right = (x, y);
            let current = match (
                region.contains(&left.into()),
                region.contains(&right.into()),
            ) {
                (false, true) => Some(Edge::Start),
                (true, false) => Some(Edge::End),
                _ => None,
            };
            if previous != current && previous.is_some() {
                num_edges += 1
            }
            previous = current;
        }
    }

    num_edges
}
#[derive(PartialEq, Eq)]
enum Edge {
    Start,
    End,
}

/// Iterate once over the coords to get all the limits
fn get_limits(region: &HashSet<Coord>) -> ((i64, i64), (i64, i64)) {
    let mut iter = region.iter();
    if let Some(first) = iter.next() {
        let (mut xmin, mut ymin) = first.into();
        let (mut xmax, mut ymax) = first.into();
        for xy in iter {
            let (x, y) = xy.into();
            if x < xmin {
                xmin = x;
            }
            if x > xmax {
                xmax = x;
            }
            if y < ymin {
                ymin = y
            }
            if y > ymax {
                ymax = y
            }
        }
        ((xmin, xmax), (ymin, ymax))
    } else {
        ((0, 0), (0, 0)) // empty region
    }
}
pub const EXAMPLE1: &str = "AAAA
BBCD
BBCC
EEEC";
pub const EXAMPLE2: &str = "RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE";
pub const EXAMPLE3: &str = "EEEEE
EXXXX
EEEEE
EXXXX
EEEEE";
pub const EXAMPLE4: &str = "AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA";

/// Use BFS to explore the region belonging to the starting coord. Return the
/// set of coords that comprises the region, and the perimeter length. The
/// latter is basically a freebie because we hit the edges during BFS, so all we
/// need to do is count them.
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
            for neighbour in coord.neighbours() {
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

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE1), 140);
        assert_eq!(part1(EXAMPLE2), 1930);
    }
    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE1), 80);
        assert_eq!(part2(EXAMPLE3), 236);
        assert_eq!(part2(EXAMPLE4), 368);
    }

    #[test]
    fn test_count_edges() {
        // X
        // XX
        //  X
        let region: HashSet<Coord> =
            HashSet::from([Coord(0, 0), Coord(0, 1), Coord(1, 1), Coord(1, 2)]);
        assert_eq!(count_edges(&region), 8);
    }
    #[test]
    fn test_count_edges_fiddly() {
        // Differentiate between start/end edges in the middle
        // X
        //  X
        let region: HashSet<Coord> = HashSet::from([Coord(0, 0), Coord(1, 1)]);
        assert_eq!(count_edges(&region), 8);
    }
}
