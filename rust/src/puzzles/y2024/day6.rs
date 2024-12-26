use std::collections::{HashMap, HashSet};

use crate::utils::SparseMatrix;

const OBSTACLE: char = '#';

// Find the number of unique squares visited by the guard
pub fn part1(input: &str) -> String {
    let mut map = parse(input);
    let guard = remove_guard(&mut map);
    let (history, _) = trace_guard(map, guard);
    let unique_positions: HashSet<Coord> = history
        .iter()
        .map(|guard| guard.position)
        .collect();
    format!("{}", unique_positions.len())
}

/// Part 2 take 2
///
/// Guard's path:
///....#.....
/// ....XXXXX#
/// ....X...X.
/// ..#.X...X.
/// ..XXXXX#X.
/// ..X.X.X.X.
/// .#XXXXXXX.
/// .XXXXXXX#.
/// #XXXXXXX..
/// ......#X..
///
/// ...<#.....
/// ...v+---+#
/// ...v|...|.
/// ..#v|...|.
/// ...v|..#|.
/// ...v|...|.
/// .#.O^---+.
/// ........#.
/// #.........
/// ......#...
///
/// ....#.....
/// ....+---+#
/// ....|...|.
/// ..#.|...|.
/// ..+-+-+#|.
/// ..|.|.|.|.
/// .#+-^-+-+.
/// .v>>>>O.#.
/// #.........
/// ......#...
///
/// ....#.....
/// ....+---+#
/// ....|...|.
/// ..#.|...|.
/// ..+-+-+#|.
/// ..|.|.|.|.
/// .#+-^-+-+.
/// .+----+O#.
/// #+----+^..
/// ......#>..
///
/// For every existing obstacle,
/// take 1 step WEST and look SOUTH. Get every intersection with the path
/// travelling WEST
///
/// take 1 step NORTH and look WEST. Get every intersection with the path
/// travelling NORTH
///
/// take 1 step EAST and look NORTH. Get every intersection with the path
/// travelling EAST
///
/// take 1 step X and look X-1. Get every intersection with the path travelling
/// X.
///
/// stop searching when you hit the first obstacle.
///
/// Once we've found this much smaller set of valid obstacle points, we check
/// all those for infinite loops.

fn scan_for_potential_obstacles(
    map: &Map,
    obstacle: &Coord,
    guard_path: &HashSet<Guard>,
) -> HashSet<Coord> {
    let mut out: HashSet<Coord> = HashSet::new();

    // Scan south
    let mut coord = obstacle.clone();
    coord = coord.west();
    loop {
        coord = coord.south();
        if !map.contains_key(&coord) {
            break;
        }
        let needle = Guard {
            position:  coord,
            direction: WEST,
        };
        if guard_path.contains(&needle) {
            out.insert(coord);
        }
    }

    // Scan north
    let mut coord = obstacle.clone();
    coord = coord.east();
    loop {
        coord = coord.north();
        if !map.contains_key(&coord) {
            break;
        }
        let needle = Guard {
            position:  coord,
            direction: EAST,
        };
        if guard_path.contains(&needle) {
            out.insert(coord);
        }
    }

    // Scan west
    let mut coord = obstacle.clone();
    coord = coord.north();
    loop {
        coord = coord.west();
        if !map.contains_key(&coord) {
            break;
        }
        let needle = Guard {
            position:  coord,
            direction: NORTH,
        };
        if guard_path.contains(&needle) {
            out.insert(coord);
        }
    }
    // Scan east
    let mut coord = obstacle.clone();
    coord = coord.south();
    loop {
        coord = coord.east();
        if !map.contains_key(&coord) {
            break;
        }
        let needle = Guard {
            position:  coord,
            direction: SOUTH,
        };
        if guard_path.contains(&needle) {
            out.insert(coord);
        }
    }
    out
}

// Insert an obstacle into every square, and check if that produces an infinite
// loop for the guard. Count the infinite loops.
pub fn part2(input: &str) -> String {
    let mut map = parse(input);
    let guard = remove_guard(&mut map);
    let (history, _) = trace_guard(map.clone(), guard.clone());
    let mut infinite_loops = 0;

    println!("The guard's path is {} long", history.len());

    let mut potential_obstacles: HashSet<Coord> = HashSet::new();
    for (obstacle, _) in map
        .iter()
        .filter(|(_, square)| square == &&OBSTACLE)
    {
        let new = scan_for_potential_obstacles(&map, obstacle, &history);
        for item in new.into_iter() {
            potential_obstacles.insert(item);
        }
    }
    println!("Found {} potential obstacles", potential_obstacles.len());

    for (ii, coord) in potential_obstacles
        .into_iter()
        .enumerate()
    {
        // not allowed to insert an obstacle at the starting point
        if coord == guard.position {
            continue;
        }
        // For every square, make a copy of the map, and try inserting an
        // obstacle
        let mut new_map = map.clone();
        new_map.insert(coord, OBSTACLE);

        // Check if there's an infinite loop
        let (_, result) = trace_guard(new_map, guard.clone());
        match result {
            TraceResult::InfiniteLoop(_) => infinite_loops += 1,
            _ => {} // do nothing for out of bounds
        }
    }

    format!("{infinite_loops}")
}

fn print_map(map: &Map) {
    let contents: HashMap<(i64, i64), char> = map
        .into_iter()
        .map(|(k, v)| ((k.x as i64, k.y as i64), *v))
        .collect();
    let matrix = SparseMatrix { contents };
    println!("{matrix}");
}

// Iterate the guard until it either goes out of bounds or enters an infinite
// loop
fn trace_guard(map: Map, guard: Guard) -> (HashSet<Guard>, TraceResult) {
    let mut history: HashSet<Guard> = HashSet::new();
    let mut guard = guard;
    loop {
        // if the guard's position is not in the map, it has gone out of bounds
        if !map.contains_key(&guard.position) {
            return (history, TraceResult::OutOfBounds(guard.position));
        }
        // if the guard assumes a position that we've seen before, it means
        // we've entered an infinite loop
        if history.contains(&guard) {
            return (history, TraceResult::InfiniteLoop(guard));
        }
        history.insert(guard.clone());
        iter_guard(&map, &mut guard);
    }
}
enum TraceResult {
    OutOfBounds(Coord),
    InfiniteLoop(Guard),
}

const EXAMPLE: &str = "....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...";

#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
struct Coord {
    x: i32,
    y: i32,
}
impl Coord {
    fn north(&self) -> Self {
        let Coord { x, y } = *self;
        Self { x, y: y - 1 }
    }
    fn south(&self) -> Self {
        let Coord { x, y } = *self;
        Self { x, y: y + 1 }
    }
    fn east(&self) -> Self {
        let Coord { x, y } = *self;
        Self { x: x + 1, y }
    }
    fn west(&self) -> Self {
        let Coord { x, y } = *self;
        Self { x: x - 1, y }
    }
}
type Map = HashMap<Coord, char>;
const NORTH: usize = 0;
const EAST: usize = 1;
const SOUTH: usize = 2;
const WEST: usize = 3;

#[derive(Hash, PartialEq, Eq, Clone)]
struct Guard {
    direction: usize,
    position:  Coord,
}
impl Guard {
    fn next_square(&self) -> Coord {
        let Coord { x, y } = self.position; // yay, destructuring sugar
        match self.direction {
            NORTH => Coord { x, y: y - 1 }, // y is positive down
            EAST => Coord { x: x + 1, y },
            SOUTH => Coord { x, y: y + 1 },
            WEST => Coord { x: x - 1, y },
            _ => unreachable!(),
        }
    }
    fn turn_right(&mut self) {
        self.direction = (self.direction + 1) % 4;
    }
    fn walk(&mut self) {
        self.position = self.next_square();
    }
}

/// Move the guard, turning if necessary. Bear in mind that we may need to turn
/// multiple times.
fn iter_guard(map: &Map, guard: &mut Guard) {
    while map.get(&guard.next_square()) == Some(&OBSTACLE) {
        guard.turn_right();
    }
    guard.walk();
}

/// Remove the guard from the map, and return its position. Assuming the guard
/// always starts facing north
fn remove_guard(map: &mut Map) -> Guard {
    for (coord, ch) in map.iter_mut() {
        if *ch == '^' {
            *ch = '.'; // set to empty
            return Guard {
                position:  coord.clone(),
                direction: NORTH,
            };
        }
    }
    unreachable!() // if no guard in map
}

fn parse(input: &str) -> HashMap<Coord, char> {
    let mut map = HashMap::new();
    for (y, row) in input.lines().enumerate() {
        for (x, ch) in row.chars().enumerate() {
            let coord = Coord {
                x: x as i32,
                y: y as i32,
            };
            map.insert(coord, ch);
        }
    }
    map
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), "41");
    }
    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), "6");
    }

    #[test]
    fn test_scan_for_potential_obstacles() {
        let mut map = parse(EXAMPLE);
        let guard = remove_guard(&mut map);
        let (guard_path, _) = trace_guard(map.clone(), guard);
        let obstacle = Coord { x: 0, y: 8 };
        assert_eq!(map.get(&obstacle), Some(&OBSTACLE));
        let potential_obstacles =
            scan_for_potential_obstacles(&map, &obstacle, &guard_path);
        for obs in potential_obstacles.iter() {
            println!("{obs:?}");
        }
        assert!(potential_obstacles.contains(&Coord { x: 7, y: 9 }));
    }
}
