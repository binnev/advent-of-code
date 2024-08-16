use crate::puzzles::y2023;
use crate::utils;
use test_case::test_case;

#[test_case("2023/day2", y2023::day2::part1, "1853")]
// #[test_case("2023/day2", y2023::day2::part2, "72706")]
#[test_case("2023/day1", y2023::day1::part1, "55123")]
#[test_case("2023/day1", y2023::day1::part2, "55260")]
fn test_2023(day: &str, func: fn(&str) -> String, expected: &str) {
    let input = utils::load_puzzle_input(day);
    let result = func(&input);
    assert_eq!(result, expected);
}
