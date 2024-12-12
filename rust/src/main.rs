#![allow(dead_code)]

mod puzzles;
mod utils;

fn main() {
    let input = crate::utils::load_puzzle_input("2024/day3");
    let result = crate::puzzles::y2024::day3::part2(&input);
    println!("{result}");
}
