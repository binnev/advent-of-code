use crate::puzzles::y2024;
use crate::utils;
use test_case::test_case;

#[test_case("2024/day1", y2024::day1::part1, "1889772")]
#[test_case("2024/day1", y2024::day1::part2, "23228917")]
#[test_case("2024/day2", y2024::day2::part1, "407")]
#[test_case("2024/day2", y2024::day2::part2, "459")]
#[test_case("2024/day3", y2024::day3::part1, "165225049")]
#[test_case("2024/day3", y2024::day3::part2, "108830766")]
fn test_2024(day: &str, func: fn(&str) -> String, expected: &str) {
    let input = utils::load_puzzle_input(day);
    let result = func(&input);
    assert_eq!(result, expected);
}
