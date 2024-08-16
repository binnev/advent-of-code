#![allow(dead_code)]

mod puzzles;
mod utils;

fn main() {
    let input = crate::utils::load_puzzle_input("2023/day2");
    let result = crate::puzzles::y2023::day2::part1(&input);
    println!("{result}");
}
