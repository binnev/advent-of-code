fn main() {
    let input = advent::utils::load_puzzle_input("2024/day19");
    let func = advent::puzzles::y2024::day19::part2;
    let result = func(&input);
    println!("{result}");
}
