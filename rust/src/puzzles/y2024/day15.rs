use std::{collections::HashSet, fmt::Display};

use crate::utils::{Coord, Direction, SparseMatrix};

pub fn part1(input: &str) -> i64 {
    let (mut map, directions) = parse(input);
    execute_robot(&mut map, directions);
    calculate_gps(&map)
}
pub fn part2(input: &str) -> i64 {
    part1(&adapt_for_part2(input))
}
fn calculate_gps(map: &SparseMatrix<char>) -> i64 {
    map.iter()
        .filter(|(_, ch)| "O[".contains(**ch))
        .map(|(Coord(x, y), _)| x + 100 * y)
        .sum()
}
fn execute_robot(map: &mut SparseMatrix<char>, directions: Vec<Direction>) {
    let mut robot: Coord = map
        .iter()
        .find(|(_, ch)| ch == &&ROBOT)
        .map(|(coord, _)| *coord)
        .expect("Couldn't find robot in map!");
    for direction in directions {
        let movable = get_movable(map, robot, &direction);
        // Only move the robot if the box(es) can move
        if movable.len() > 0 {
            robot = robot.neighbour(direction);
        }
        shift(map, movable, direction);
    }
}
/// Check if the given shift is possible. Return the set of coords that will be
/// affected by the shift, if it is possible.
fn get_movable(
    map: &mut SparseMatrix<char>,
    coord: Coord,
    direction: &Direction,
) -> HashSet<Coord> {
    let target = coord.neighbour(*direction);
    let mut movable: HashSet<Coord> = HashSet::new();
    match map.get(&target) {
        // Base cases -- empty space or wall
        Some(&WALL) => return movable,
        None => {
            movable.insert(coord);
            return movable;
        }

        // ----- Recursive cases -----
        // Boxes always move 1-wide
        Some(&BOX) => {
            let knock_on = get_movable(map, target, direction);
            if knock_on.len() > 0 {
                movable.insert(coord);
                movable.extend(knock_on);
            }
            return movable;
        }
        // Wide boxes behave normally in horizontal movement
        Some(&BOX_LEFT) | Some(&BOX_RIGHT) if direction.is_horizontal() => {
            let knock_on = get_movable(map, target, direction);
            if knock_on.len() > 0 {
                movable.insert(coord);
                movable.extend(knock_on);
            }
            return movable;
        }
        // Wide box vertical movement -- take into account the other half of the
        // box too. A move is only possible if _both_ halves of the box are able
        // to move.
        Some(&BOX_LEFT) | Some(&BOX_RIGHT) => {
            let target_neighbour = match map.get(&target) {
                Some(&BOX_LEFT) => target.neighbour(Direction::East),
                Some(&BOX_RIGHT) => target.neighbour(Direction::West),
                _ => unreachable!(),
            };
            let knock_on1 = get_movable(map, target, direction);
            let knock_on2 = get_movable(map, target_neighbour, direction);
            if knock_on1.len() > 0 && knock_on2.len() > 0 {
                movable.insert(coord);
                movable.extend(knock_on1);
                movable.extend(knock_on2);
            }
            return movable;
        }

        Some(other) => panic!("Unexpected object in map: {other}"),
    }
}
/// Moving them one at a time might result in overwrites.
fn shift(
    map: &mut SparseMatrix<char>,
    coords: HashSet<Coord>,
    direction: Direction,
) {
    let removed: Vec<_> = coords
        .into_iter()
        .map(|coord| {
            (
                coord,
                map.remove(&coord)
                    .expect("Tried to remove nonexistent entry!"),
            )
        })
        .collect();
    removed
        .into_iter()
        .for_each(|(coord, ch)| {
            let target = coord.neighbour(direction);
            map.insert(target, ch);
        });
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
fn adapt_for_part2(input: &str) -> String {
    input
        .chars()
        .map(|ch| match ch {
            '#' => "##".into(),
            'O' => "[]".into(),
            '.' => "..".into(),
            '@' => "@.".into(),
            _ => ch.to_string(),
        })
        .collect()
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
        assert_eq!(part2(EXAMPLE), 9021);
    }
    #[test]
    fn test_execute_robot() {
        let (mut map, directions) = parse(EXAMPLE2);
        let (expected, _) = parse(&(EXAMPLE2_COMPLETED.to_owned() + "\n\n"));
        execute_robot(&mut map, directions);
        assert_eq!(map, expected);
    }
    #[test]
    fn test_calculate_gps() {
        assert_eq!(calculate_gps(&GPS_EXAMPLE.into()), 104);
        assert_eq!(calculate_gps(&EXAMPLE2_COMPLETED.into()), 2028);
        assert_eq!(calculate_gps(&EXAMPLE_COMPLETED.into()), 10092);
        assert_eq!(calculate_gps(&GPS_EXAMPLE2.into()), 105);
    }
    #[test]
    fn test_adapt_for_part2() {
        let expected = "####################
##....[]....[]..[]##
##............[]..##
##..[][]....[]..[]##
##....[]@.....[]..##
##[]##....[]......##
##[]....[]....[]..##
##..[][]..[]..[][]##
##........[]......##
####################

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
        let adapted = adapt_for_part2(EXAMPLE);
        assert_eq!(adapted, expected);
    }
}

const ROBOT: char = '@';
const WALL: char = '#';
const BOX: char = 'O';
const BOX_LEFT: char = '[';
const BOX_RIGHT: char = ']';

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
const EXAMPLE_SCALED_COMPLETED: &str = "####################
##[].......[].[][]##
##[]...........[].##
##[]........[][][]##
##[]......[]....[]##
##..##......[]....##
##..[]............##
##..@......[].[][]##
##......[][]..[]..##
####################";
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
const GPS_EXAMPLE2: &str = "##########
##...[]...
##........";
const EXAMPLE3: &str = "#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^";
const EXAMPLE3_SCALED: &str = "##############
##......##..##
##..........##
##....[][]@.##
##....[]....##
##..........##
##############";
const EXAMPLE3_SCALED_COMPLETED: &str = "##############
##...[].##..##
##...@.[]...##
##....[]....##
##..........##
##..........##
##############";
