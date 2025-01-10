#![allow(dead_code)]

mod puzzles;
mod utils;

fn main() {
    let input = crate::utils::load_puzzle_input("2024/day11");
    let result = crate::puzzles::y2024::day11::part1(&input);
    println!("{result}");
}
