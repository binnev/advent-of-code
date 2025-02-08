fn main() {
    let input = advent::utils::load_puzzle_input("2024/day21");
    let func = advent::puzzles::y2024::day21::part1;
    let result = func(&input);
    println!("{result}");
}
