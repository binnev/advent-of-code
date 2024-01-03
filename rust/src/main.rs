mod puzzles;
mod utils;

fn main() {
    let input = crate::utils::load_puzzle_input("2023/day1");
    let result = crate::puzzles::y2023::day1::part1(&input);
    println!("{result}");
}
