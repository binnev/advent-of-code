use regex::Regex;

use crate::utils::Coord;

const COST_A: i64 = 3;
const COST_B: i64 = 1;
const FUDGE: i64 = 10000000000000;

pub fn part1(input: &str) -> i64 {
    let claw_machines = parse(input);
    let mut out = 0;
    for (Coord(xa, ya), Coord(xb, yb), Coord(xp, yp)) in claw_machines {
        if let Some((na, nb)) = solve(xa, ya, xb, yb, xp, yp) {
            out += solution_cost(na, nb);
        }
    }
    out
}
pub fn part2(input: &str) -> i64 {
    let claw_machines = parse(input);
    let mut out = 0;
    for (Coord(xa, ya), Coord(xb, yb), Coord(xp, yp)) in claw_machines {
        if let Some((na, nb)) = solve(xa, ya, xb, yb, xp + FUDGE, yp + FUDGE) {
            out += solution_cost(na, nb);
        }
    }
    out
}
/// This is going to be solving simultaneous equations.
/// 1: xa * na + xb + nb = x_prize
/// 2: ya * na + yb * nb = y_prize
///
/// knowns: xa, ya, xb, yb, x_prize, y_prize
/// unknowns: na, nb
/// equations: 2
///
/// Solve the simultaneous equations and calculate na & nb in terms of
/// floats. Round them to the nearest integer. Check the solution to make
/// sure it is a valid integer solution.
fn solve(
    xa: i64,
    ya: i64,
    xb: i64,
    yb: i64,
    xp: i64,
    yp: i64,
) -> Option<(i64, i64)> {
    let (na, nb) = {
        let xa = xa as f64;
        let ya = ya as f64;
        let xb = xb as f64;
        let yb = yb as f64;
        let xp = xp as f64;
        let yp = yp as f64;

        // Solve 1 & 2 for na
        let na = -(xp / xb - yp / yb) / (ya / yb - xa / xb);
        let na = na.round() as i64;

        // Solve 1 for nb
        let nb = ((xp - xa * na as f64) / xb).trunc() as i64;
        (na, nb)
    };
    if check_solution(Coord(xa, ya), Coord(xb, yb), Coord(xp, yp), na, nb) {
        Some((na, nb))
    } else {
        None
    }
}
fn check_solution(
    button_a: Coord,
    button_b: Coord,
    prize: Coord,
    na: i64,
    nb: i64,
) -> bool {
    let (xa, ya) = button_a.into();
    let (xb, yb) = button_b.into();
    let x = xa * na + xb * nb;
    let y = ya * na + yb * nb;
    (x, y) == prize.into()
}
fn solution_cost(na: i64, nb: i64) -> i64 {
    na * COST_A + nb * COST_B
}
fn parse(input: &str) -> Vec<(Coord, Coord, Coord)> {
    input
        .split("\n\n")
        .map(|chunk| parse_machine(chunk).unwrap())
        .collect()
}
fn parse_machine(chunk: &str) -> Option<(Coord, Coord, Coord)> {
    let mut lines = chunk.lines();
    let line_a = lines.next().unwrap();
    let line_b = lines.next().unwrap();
    let line_p = lines.next().unwrap();
    let button_a = parse_line_xy(line_a)?;
    let button_b = parse_line_xy(line_b)?;
    let prize = parse_line_xy(line_p)?;
    Some((button_a, button_b, prize))
}
fn parse_line_xy(line: &str) -> Option<Coord> {
    let rx = Regex::new(r".*X.(\d+), Y.(\d+)").unwrap();
    let caps = rx.captures(line).unwrap();
    let x = caps.get(1)?.as_str().parse().ok()?;
    let y = caps.get(2)?.as_str().parse().ok()?;
    Some(Coord(x, y))
}
const EXAMPLE: &str = "Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279";

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 480);
    }
    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 875318608908);
    }

    #[test]
    fn test_solve() {
        let machines = parse(EXAMPLE);
        let expected_results = [Some((80, 40)), None, Some((38, 86)), None];
        for (machine, expected) in machines
            .into_iter()
            .zip(expected_results)
        {
            let (Coord(xa, ya), Coord(xb, yb), Coord(xp, yp)) = machine;
            assert_eq!(solve(xa, ya, xb, yb, xp, yp), expected);
        }
    }

    #[test]
    fn test_solve_more() {
        // Machine 313
        let (xa, ya) = (63, 12);
        let (xb, yb) = (23, 90);
        let (xp, yp) = (3708, 3018);
        let expected = Some((49, 27));
        assert_eq!(solve(xa, ya, xb, yb, xp, yp), expected);

        // Machine 76
        let (xa, ya) = (72, 45);
        let (xb, yb) = (17, 36);
        let (xp, yp) = (4731, 8729);
        let expected = None;
        assert_eq!(solve(xa, ya, xb, yb, xp, yp), expected);
    }

    #[test]
    fn test_parse_line_xy() {
        assert_eq!(
            parse_line_xy("Button A: X+94, Y+34").unwrap(),
            Coord(94, 34)
        );
        assert_eq!(
            parse_line_xy("Prize: X=8400, Y=5400").unwrap(),
            Coord(8400, 5400)
        );
    }
}
