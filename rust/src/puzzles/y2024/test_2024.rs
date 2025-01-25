use std::fmt::Debug;
use std::time::Instant;

use crate::puzzles::y2024;
use crate::utils;
use test_case::test_case;

#[test_case("2024/day1", y2024::day1::part1, 1889772)]
#[test_case("2024/day1", y2024::day1::part2, 23228917)]
#[test_case("2024/day2", y2024::day2::part1, 407)]
#[test_case("2024/day2", y2024::day2::part2, 459)]
#[test_case("2024/day3", y2024::day3::part1, 165225049)]
#[test_case("2024/day3", y2024::day3::part2, 108830766)]
#[test_case("2024/day4", y2024::day4::part1, 2642)]
#[test_case("2024/day4", y2024::day4::part2, 1974)]
#[test_case("2024/day5", y2024::day5::part1, 4790)]
#[test_case("2024/day6", y2024::day6::part1, 5030)]
#[test_case("2024/day6", y2024::day6::part2, 1928)]
#[test_case("2024/day7", y2024::day7::part1, 1260333054159)]
#[test_case("2024/day7", y2024::day7::part2, 162042343638683)]
#[test_case("2024/day8", y2024::day8::part1, 249)]
#[test_case("2024/day8", y2024::day8::part2, 905)]
#[test_case("2024/day9", y2024::day9::part1, 6349606724455)]
#[test_case("2024/day9", y2024::day9::part2, 6376648986651)]
#[test_case("2024/day10", y2024::day10::part1, 674)]
#[test_case("2024/day10", y2024::day10::part2, 1372)]
#[test_case("2024/day11", y2024::day11::part1, 199753)]
#[test_case("2024/day12", y2024::day12::part1, 1533024)]
#[test_case("2024/day12", y2024::day12::part2, 910066)]
#[test_case("2024/day13", y2024::day13::part1, 26599)]
#[test_case("2024/day13", y2024::day13::part2, 106228669504887)]
#[test_case("2024/day14", y2024::day14::part1, 230436441)]
#[test_case("2024/day14", y2024::day14::part2, 8270)]
#[test_case("2024/day15", y2024::day15::part1, 1412971)]
#[test_case("2024/day15", y2024::day15::part2, 1429299)]
#[test_case("2024/day16", y2024::day16::part1, 85396)]
#[test_case("2024/day16", y2024::day16::part2, 428)]
#[test_case("2024/day17", y2024::day17::part1, "1,5,7,4,1,6,0,3,0")]
#[test_case("2024/day18", y2024::day18::part1, 454)]
#[test_case("2024/day18", y2024::day18::part2, "8,51")]
fn test_2024<Output, Expected>(
    day: &str,
    func: fn(&str) -> Output,
    expected: Expected,
) where
    Output: Debug + PartialEq<Expected>,
    Expected: Debug,
{
    let input = utils::load_puzzle_input(day);
    let result = func(&input);
    assert_eq!(result, expected);
}
