use std::collections::{HashMap, HashSet};

pub fn part1(input: &str) -> String {
    let mut map = parse(input);
    let mut guard = remove_guard(&mut map);
    let mut visited: HashSet<Coord, _> = HashSet::new();
    while map.contains_key(&guard.position) {
        visited.insert(guard.position);
        iter_guard(&map, &mut guard);
    }
    format!("{}", visited.len())
}
pub fn part2(input: &str) -> String {
    "".into()
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
type Map = HashMap<Coord, char>;
const NORTH: usize = 0;
const EAST: usize = 1;
const SOUTH: usize = 2;
const WEST: usize = 3;

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
    while map.get(&guard.next_square()) == Some(&'#') {
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
        assert_eq!(part2(EXAMPLE), "");
    }
}
