use regex::Regex;

use crate::utils::Coord;

pub fn part1(input: &str) -> usize {
    do_the_thing(input, 100, (101, 103))
}
pub fn part2(input: &str) -> usize {
    0
}
fn do_the_thing(input: &str, steps: i64, limits: Coord) -> usize {
    let robots = parse(input);
    let truncated_positions: Vec<Coord> = robots
        .iter()
        .map(|robot| simulate_robot(robot, steps, limits))
        .collect();
    count_robots(&truncated_positions, limits)
}
/// Count how many robots are in each quadrant
fn count_robots(positions: &Vec<Coord>, limits: Coord) -> usize {
    let (xlim, ylim) = limits;
    assert!(xlim % 2 != 0); // limits should be odd
    assert!(ylim % 2 != 0);
    let middle_x = xlim / 2;
    let middle_y = ylim / 2;
    let (mut topleft, mut topright, mut btmleft, mut btmright) = (0, 0, 0, 0);
    for (x, y) in positions {
        let dx = x - middle_x;
        let dy = y - middle_y;
        if dx < 0 && dy < 0 {
            topleft += 1
        } else if dx > 0 && dy < 0 {
            topright += 1
        } else if dx < 0 && dy > 0 {
            btmleft += 1
        } else if dx > 0 && dy > 0 {
            btmright += 1
        }
    }
    topleft * topright * btmleft * btmright
}
/// Calculate the robot's position after the given number of steps
fn simulate_robot(robot: &Robot, steps: i64, limits: Coord) -> Coord {
    let (mut x, mut y) = robot.position;
    let (u, v) = robot.velocity;
    let (xlim, ylim) = limits;
    x += u * steps;
    y += v * steps;
    // todo: wrapping
    x = wrap(x, xlim);
    y = wrap(y, ylim);
    (x, y)
}
fn wrap(x: i64, limit: i64) -> i64 {
    let mut x = x;
    x %= limit;
    if x < 0 {
        x += limit
    }
    x
}
#[derive(PartialEq, Eq, Debug)]
struct Robot {
    position: Coord,
    velocity: Coord,
}
fn parse(input: &str) -> Vec<Robot> {
    input
        .lines()
        .map(|line| parse_line(line).unwrap())
        .collect()
}
fn parse_line(line: &str) -> Option<Robot> {
    let rx = Regex::new(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)").unwrap();
    let caps = rx.captures(line)?;
    let x = caps.get(1)?.as_str().parse().ok()?;
    let y = caps.get(2)?.as_str().parse().ok()?;
    let u = caps.get(3)?.as_str().parse().ok()?;
    let v = caps.get(4)?.as_str().parse().ok()?;
    Some(Robot {
        position: (x, y),
        velocity: (u, v),
    })
}
const EXAMPLE: &str = "p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3";
#[cfg(test)]
mod tests {
    use std::collections::HashSet;

    use crate::utils::SparseMatrix;

    use super::*;
    #[test]
    fn test_part1() {
        let limits = (11, 7);
        assert_eq!(do_the_thing(EXAMPLE, 100, limits), 12);
    }
    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 0);
    }
    #[test]
    fn test_parse_line() {
        let line = "p=2,4 v=2,-3";
        let expected = Robot {
            position: (2, 4),
            velocity: (2, -3),
        };
        assert_eq!(parse_line(line).unwrap(), expected);
    }
    #[test]
    fn test_parse() {
        let expected_str = "1.12.......
...........
...........
......11.11
1.1........
.........1.
.......1...";
        let tmp: SparseMatrix<char> = expected_str.into();
        let expected = SparseMatrix {
            contents: tmp
                .clone()
                .into_iter()
                .filter(|(_, v)| *v != '.')
                .map(|(k, v)| (k, v.to_digit(10).unwrap()))
                .collect(),
        };
        let robots = parse(EXAMPLE);
        let mut map: SparseMatrix<u32> = SparseMatrix::new();
        for r in robots {
            map.entry(r.position)
                .and_modify(|e| *e += 1)
                .or_insert(1);
        }
        assert_eq!(map, expected);
    }
    #[test]
    fn test_wrap() {
        let width = 5;
        assert_eq!(wrap(0, width), 0);
        assert_eq!(wrap(4, width), 4); // 4 is the last pos in a 5-wide array
        assert_eq!(wrap(5, width), 0); // 5 should wrap back to 0
        assert_eq!(wrap(-1, width), 4); // -1 should wrap back to 4
        assert_eq!(wrap(-2, width), 3);
        assert_eq!(wrap(-3, width), 2);
        assert_eq!(wrap(-4, width), 1);
        assert_eq!(wrap(-5, width), 0);
        assert_eq!(wrap(-6, width), 4); // multiple wraps should work
    }
}
