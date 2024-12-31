use std::time::Instant;

use crate::puzzles::y2024;
use crate::utils;
use test_case::test_case;

#[test_case("2024/day1", y2024::day1::part1, "1889772")]
#[test_case("2024/day1", y2024::day1::part2, "23228917")]
#[test_case("2024/day2", y2024::day2::part1, "407")]
#[test_case("2024/day2", y2024::day2::part2, "459")]
#[test_case("2024/day3", y2024::day3::part1, "165225049")]
#[test_case("2024/day3", y2024::day3::part2, "108830766")]
#[test_case("2024/day4", y2024::day4::part1, "2642")]
#[test_case("2024/day4", y2024::day4::part2, "1974")]
#[test_case("2024/day5", y2024::day5::part1, "4790")]
#[test_case("2024/day6", y2024::day6::part1, "5030")]
#[test_case("2024/day6", y2024::day6::part2, "1928")]
#[test_case("2024/day7", y2024::day7::part1, "1260333054159")]
#[test_case("2024/day7", y2024::day7::part2, "162042343638683")]
#[test_case("2024/day8", y2024::day8::part1, "249")]
#[test_case("2024/day8", y2024::day8::part2, "905")]
#[test_case("2024/day9", y2024::day9::part1, "6349606724455")]
fn test_2024(day: &str, func: fn(&str) -> String, expected: &str) {
    let input = utils::load_puzzle_input(day);
    let start = Instant::now();
    let result = func(&input);
    let duration = start.elapsed();
    println!("Got {result} in {duration:?}");
    assert_eq!(result, expected);
}
