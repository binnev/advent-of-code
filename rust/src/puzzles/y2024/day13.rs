use regex::Regex;

use crate::utils::Coord;

const COST_A: i64 = 3;
const COST_B: i64 = 1;

/// The claw machines here are a little unusual. Instead of a joystick or
/// directional buttons to control the claw, these machines have two buttons
/// labeled A and B. Worse, you can't just put in a token and play; it costs 3
/// tokens to push the A button and 1 token to push the B button.
///
/// This is going to be solving simultaneous equations.
/// 1: xa * na + xb + nb = x_prize
/// 2: ya * na + yb * nb = y_prize
///
/// knowns: xa, ya, xb, yb, x_prize, y_prize
/// unknowns: na, nb
/// equations: 2
///
/// 1:
/// xa.na + xb.nb = x_prize
/// na + xb.nb/xa = x_prize/xa
/// na = x_prize/xa - xb.nb/xa
///
/// 2:
/// ya.na + yb.nb = y_prize
/// na + yb.nb/ya = y_prize/ya
///
/// sub in 1:
/// (x_prize/xa - xb.nb/xa) + yb.nb/ya = y_prize/ya
///
/// solve for nb:
/// x_prize/xa - xb.nb/xa + yb.nb/ya = y_prize/ya
/// x_prize/xa - nb(xb/xa + yb/ya) = y_prize/ya
/// - nb(xb/xa + yb/ya) = y_prize/ya - x_prize/xa
/// nb(xb/xa + yb/ya) = x_prize/xa - y_prize/ya
/// nb = (x_prize/xa - y_prize/ya) / (xb/xa + yb/ya)
///
/// try it for this example:
/// xa = 94, ya = 34
/// xb = 22, yb = 67
/// x_prize = 8400, y_prize = 5400
/// nb = (8400/94 - 5400/34) / (22/94 + 67/34)
///
/// The key is it must be an _integer_ solution.
///
///
///
///  
///
/// It all looks linear -- so how can there be multiple solutions? It's probably
/// 2 planes intersecting or something.
///
///
/// |     nb
/// |    /
/// |   /
/// |  /
/// | /
/// |/_______ na
pub fn part1(input: &str) -> i64 {
    let claw_machines = parse(input);
    let mut out = 0;
    for (button_a, button_b, prize) in claw_machines {
        brute_force_solutions(button_a, button_b, prize)
            .iter()
            .min_by(|(cost_a, _), (cost_b, _)| cost_a.cmp(&cost_b))
            .map(|(cost, _)| out += cost);
    }
    out
}
pub fn part2(input: &str) -> usize {
    0
}
fn solve(xa: f64, ya: f64, xb: f64, yb: f64, xp: f64, yp: f64) -> f64 {
    -(xp / xb - yp / yb) / (ya / yb - xa / xb)
}

fn brute_force_solutions(
    button_a: Coord,
    button_b: Coord,
    prize: Coord,
) -> Vec<(i64, Coord)> {
    let (xa, ya) = button_a;
    let (xb, yb) = button_b;
    let mut solutions = vec![];
    for na in 0..=100 {
        for nb in 0..=100 {
            let x = xa * na + xb * nb;
            let y = ya * na + yb * nb;
            let position = (x, y);
            if position == prize {
                let cost = na * COST_A + nb * COST_B;
                solutions.push((cost, (na, nb)));
            }
        }
    }
    solutions
}
fn parse(input: &str) -> Vec<(Coord, Coord, Coord)> {
    let mut out = vec![];
    for chunk in input.split("\n\n") {
        let mut lines = chunk.lines();
        let line_a = lines.next().unwrap();
        let line_b = lines.next().unwrap();
        let line_p = lines.next().unwrap();
        let (xa, ya) = parse_line_xy(line_a);
        let (xb, yb) = parse_line_xy(line_b);
        let (xp, yp) = parse_line_xy(line_p);
        out.push(((xa, ya), (xb, yb), (xp, yp)));
    }
    out
}

fn parse_line_xy(line: &str) -> Coord {
    let rx = Regex::new(r".*X.(\d+), Y.(\d+)").unwrap();
    let caps = rx.captures(line).unwrap();
    let x = caps
        .get(1)
        .unwrap()
        .as_str()
        .parse()
        .unwrap();
    let y = caps
        .get(2)
        .unwrap()
        .as_str()
        .parse()
        .unwrap();
    (x, y)
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
        assert_eq!(part2(EXAMPLE), 0);
    }

    // #[test]
    // fn test_solve() {
    //     let xa = 94f64;
    //     let ya = 34f64;
    //     let xb = 22f64;
    //     let yb = 67f64;
    //     let xp = 8400f64;
    //     let yp = 5400f64;
    //     let result = solve(xa, ya, xb, yb, xp, yp);
    //     assert_eq!(result, 80f64);
    // }

    #[test]
    fn test_parse_line_xy() {
        assert_eq!(parse_line_xy("Button A: X+94, Y+34"), (94, 34));
        assert_eq!(parse_line_xy("Prize: X=8400, Y=5400"), (8400, 5400));
    }
}
