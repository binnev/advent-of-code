use crate::puzzles::y2023;
use crate::utils;
use test_case::test_case;

#[test_case("2023/day1", y2023::day1::part1, "55123")]
#[test_case("2023/day1", y2023::day1::part2, "")]
fn test_2023(day: &str, func: fn(&str) -> String, expected: &str) {
    let input = utils::load_puzzle_input(day);
    let result = func(&input);
    assert_eq!(result, expected);
}
