use std::fmt::Debug;
use std::time::Instant;

use crate::puzzles::y2024;
use crate::utils;
use test_case::test_case;

#[test_case("2024/day1", y2024::day1::part1, "1889772".into())]
#[test_case("2024/day1", y2024::day1::part2, "23228917".into())]
#[test_case("2024/day2", y2024::day2::part1, "407".into())]
#[test_case("2024/day2", y2024::day2::part2, "459".into())]
#[test_case("2024/day3", y2024::day3::part1, "165225049".into())]
#[test_case("2024/day3", y2024::day3::part2, "108830766".into())]
#[test_case("2024/day4", y2024::day4::part1, "2642".into())]
#[test_case("2024/day4", y2024::day4::part2, "1974".into())]
#[test_case("2024/day5", y2024::day5::part1, "4790".into())]
#[test_case("2024/day6", y2024::day6::part1, "5030".into())]
#[test_case("2024/day6", y2024::day6::part2, "1928".into())]
#[test_case("2024/day7", y2024::day7::part1, "1260333054159".into())]
#[test_case("2024/day7", y2024::day7::part2, "162042343638683".into())]
#[test_case("2024/day8", y2024::day8::part1, "249".into())]
#[test_case("2024/day8", y2024::day8::part2, "905".into())]
#[test_case("2024/day9", y2024::day9::part1, "6349606724455".into())]
#[test_case("2024/day9", y2024::day9::part2, "6376648986651".into())]
#[test_case("2024/day10", y2024::day10::part1, 674)]
fn test_2024<T: Debug + Eq>(day: &str, func: fn(&str) -> T, expected: T) {
    let input = utils::load_puzzle_input(day);
    let start = Instant::now();
    let result = func(&input);
    let duration = start.elapsed();
    println!("Got {result:?} in {duration:?}");
    assert_eq!(result, expected);
}
