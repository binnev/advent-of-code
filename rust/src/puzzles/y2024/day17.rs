use std::ops::BitXor;

use itertools::Itertools;

pub fn part1(input: &str) -> String {
    let (mut state, program) = parse(input).unwrap();
    compute(&mut state, program);
    state.out.iter().join(",")
}
pub fn part2(input: &str) -> String {
    "".into()
}
fn compute(state: &mut State, program: &str) -> Option<()> {
    let program: Vec<usize> = program
        .split(",")
        .into_iter()
        .map(|s| {
            s.parse()
                .expect(&format!("Couldn't parse {s}"))
        })
        .collect();

    loop {
        let opcode = program.get(state.instruction)?;
        let operand = *program.get(state.instruction + 1)?;
        state.jumped = false;
        let func = match opcode {
            0 => adv,
            1 => bxl,
            2 => bst,
            3 => jnz,
            4 => bxc,
            5 => out,
            6 => bdv,
            7 => cdv,
            _ => todo!(),
        };
        func(state, operand);
        if !state.jumped {
            state.instruction += 2;
        }
    }
    unreachable!()
}
fn bxl(state: &mut State, operand: usize) {
    state.b = state.b ^ operand
}
fn bst(state: &mut State, operand: usize) {
    state.b = combo(state, operand) % 8;
}
fn jnz(state: &mut State, operand: usize) {
    if state.a != 0 {
        state.instruction = operand;
        state.jumped = true;
    }
}
fn bxc(state: &mut State, operand: usize) {
    state.b = state.b ^ state.c;
}
fn out(state: &mut State, operand: usize) {
    let output = combo(state, operand) % 8;
    state.out.push(output);
}
fn adv(state: &mut State, operand: usize) {
    state.a = divide(state, operand);
}
fn bdv(state: &mut State, operand: usize) {
    state.b = divide(state, operand);
}
fn cdv(state: &mut State, operand: usize) {
    state.c = divide(state, operand);
}
fn divide(state: &mut State, operand: usize) -> usize {
    let numerator = state.a;
    let exponent = combo(state, operand) as u32;
    let denominator = 2usize.pow(exponent);
    numerator / denominator
}
fn combo(state: &mut State, operand: usize) -> usize {
    match operand {
        0..=3 => operand, // literal operand
        4 => state.a,
        5 => state.b,
        6 => state.c,
        _ => unreachable!(),
    }
}
fn parse(input: &str) -> Option<(State, &str)> {
    let mut parts = input.split("\n\n");
    let register_part = parts.next()?;
    let mut register_lines = register_part.lines();
    let state = State {
        a: parse_register(register_lines.next()?)?,
        b: parse_register(register_lines.next()?)?,
        c: parse_register(register_lines.next()?)?,
        ..State::default()
    };

    let program = parts
        .next()?
        .split_whitespace()
        .last()?;
    Some((state, program.trim()))
}
fn parse_register(input: &str) -> Option<usize> {
    Some(
        input
            .split_whitespace()
            .last()?
            .parse()
            .unwrap(),
    )
}
#[derive(Default, Debug, PartialEq)]
struct State {
    a:           usize,
    b:           usize,
    c:           usize,
    out:         Vec<usize>,
    instruction: usize,
    jumped:      bool,
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), "4,6,3,5,6,3,5,2,1,0");
    }
    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), "");
    }

    #[test]
    fn test_computer() {
        let mut state = State {
            c: 9,
            ..Default::default()
        };
        compute(&mut state, "2,6");
        assert_eq!(state.b, 1);

        let mut state = State {
            a: 10,
            ..Default::default()
        };
        compute(&mut state, "5,0,5,1,5,4");
        assert_eq!(state.out, [0, 1, 2]);

        let mut state = State {
            a: 2024,
            ..Default::default()
        };
        compute(&mut state, "0,1,5,4,3,0");
        assert_eq!(state.out, [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]);
        assert_eq!(state.a, 0);

        let mut state = State {
            b: 29,
            ..Default::default()
        };
        compute(&mut state, "1,7");
        assert_eq!(state.b, 26);

        let mut state = State {
            b: 2024,
            c: 43690,
            ..Default::default()
        };
        compute(&mut state, "4,0");
        assert_eq!(state.b, 44354);
    }
}
const EXAMPLE: &str = "Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0";
