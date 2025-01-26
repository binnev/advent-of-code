#![allow(dead_code)]
#![allow(unused)]

mod puzzles;
mod utils;

fn main() {
    let input = crate::utils::load_puzzle_input("2024/day19");
    let result = crate::puzzles::y2024::day19::part2(&input);
    println!("{result}");
}
