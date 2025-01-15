use std::fmt::Display;

use crate::utils::{Coord, SparseMatrix};

pub fn part1(input: &str) -> i64 {
    let (mut map, directions) = parse(input);
    execute_robot(&mut map, directions);
    calculate_gps(&map)
}
pub fn part2(input: &str) -> usize {
    0
}
fn calculate_gps(map: &SparseMatrix<char>) -> i64 {
    map.iter()
        .filter(|(_, ch)| ch == &&BOX)
        .map(|((x, y), _)| x + 100 * y)
        .sum()
}
fn execute_robot(map: &mut SparseMatrix<char>, directions: Vec<Direction>) {
    let mut robot: Coord = map
        .iter()
        .find(|(_, ch)| ch == &&ROBOT)
        .map(|(coord, _)| *coord)
        .expect("Couldn't find robot in map!");
    for direction in directions {
        if let Some(new_robot) = shift_if_possible(map, robot, &direction) {
            robot = new_robot;
        }
    }
}
/// Try to move the object at `coord` in the specified direction. Also move any
/// objects in the way, if possible. Return the new Coord if the move was
/// possible, None otherwise.
fn shift_if_possible(
    map: &mut SparseMatrix<char>,
    coord: Coord,
    direction: &Direction,
) -> Option<Coord> {
    let target = get_neighbour(coord, direction);
    match map.get(&target) {
        // Base cases -- empty space or wall
        Some(&WALL) => return None,
        None => {
            // empty space
            shift(map, coord, target);
            return Some(target);
        }

        // Recursive case -- box in the way. Try to move that box first.
        Some(&BOX) => {
            let possible = shift_if_possible(map, target, direction);
            if possible.is_some() {
                // If it was possible to move the box, also move the current
                // object.
                shift(map, coord, target);
                return Some(target);
            } else {
                return None;
            }
        }

        Some(other) => panic!("Unexpected object in map: {other}"),
    }
}
fn shift(map: &mut SparseMatrix<char>, from: Coord, to: Coord) {
    let obj = map
        .remove(&from)
        .expect("Trying to move empty space!");
    map.insert(to, obj);
}
fn get_neighbour((x, y): Coord, direction: &Direction) -> Coord {
    match direction {
        Direction::North => (x, y - 1),
        Direction::South => (x, y + 1),
        Direction::West => (x - 1, y),
        Direction::East => (x + 1, y),
    }
}
fn parse(input: &str) -> (SparseMatrix<char>, Vec<Direction>) {
    let mut parts = input.split("\n\n");

    // Parse map. Remove the '.' characters so that we don't have to
    // differentiate between empty and '.'
    let map_str = parts.next().unwrap();
    let mut map: SparseMatrix<char> = map_str.into();
    map.contents = map
        .contents
        .into_iter()
        .filter(|(_, ch)| ch != &'.')
        .collect();

    let directions_str = parts.next().unwrap();
    let directions = directions_str
        .chars()
        .filter(|ch| "<>v^".contains(*ch)) // ignore newlines
        .map(|ch| match ch {
            '<' => Direction::West,
            '>' => Direction::East,
            '^' => Direction::North,
            'v' => Direction::South,
            _ => unreachable!(),
        })
        .collect();
    (map, directions)
}
#[derive(PartialEq, Eq, Debug)]
enum Direction {
    North,
    East,
    South,
    West,
}
impl Display for Direction {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let ch = match self {
            Self::East => '>',
            Self::West => '<',
            Self::North => '^',
            Self::South => 'v',
        };
        write!(f, "{ch}")
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 10092);
    }
    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 0);
    }

    #[test]
    fn test_execute_robot() {
        let (mut map, directions) = parse(EXAMPLE2);
        let (expected, _) = parse(&(EXAMPLE2_COMPLETED.to_owned() + "\n\n>"));
        execute_robot(&mut map, directions);
        assert_eq!(map, expected);
    }
    #[test]
    fn test_calculate_gps() {
        assert_eq!(calculate_gps(&GPS_EXAMPLE.into()), 104);
        assert_eq!(calculate_gps(&EXAMPLE2_COMPLETED.into()), 2028);
        assert_eq!(calculate_gps(&EXAMPLE_COMPLETED.into()), 10092);
    }
}

const ROBOT: char = '@';
const WALL: char = '#';
const BOX: char = 'O';
const EXAMPLE: &str = "##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^";
const EXAMPLE_COMPLETED: &str = "##########
#.O.O.OOO#
#........#
#OO......#
#OO@.....#
#O#.....O#
#O.....OO#
#O.....OO#
#OO....OO#
##########";
const EXAMPLE2: &str = "########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<";
const EXAMPLE2_COMPLETED: &str = "########
#....OO#
##.....#
#.....O#
#.#O@..#
#...O..#
#...O..#
########";
const GPS_EXAMPLE: &str = "#######
#...O..
#......";
