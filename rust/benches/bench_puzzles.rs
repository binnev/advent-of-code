use advent::puzzles::{y2023, y2024};
use advent::utils;
use advent::{expand, utils::split_path};
use criterion::{criterion_group, criterion_main, Criterion};
use std::fmt::Debug;

/// Benchmark all the puzzles with their full input.
/// Filter for a specific year/day/part by passing it to cargo bench e.g.:
/// cargo bench puzzle/2024
/// cargo bench puzzle/2024/day1
/// cargo bench puzzle/2024/day1/part1
pub fn bench_puzzles(c: &mut Criterion) {
    // ----- 2023 -----
    bench_puzzle(c, expand!(y2023::day2::part1), "1853");
    bench_puzzle(c, expand!(y2023::day2::part2), "72706");
    bench_puzzle(c, expand!(y2023::day1::part1), "55123");
    bench_puzzle(c, expand!(y2023::day1::part2), "55260");

    // ----- 2024 -----
    bench_puzzle(c, expand!(y2024::day1::part1), 1889772);
    bench_puzzle(c, expand!(y2024::day1::part2), 23228917);
    bench_puzzle(c, expand!(y2024::day2::part1), 407);
    bench_puzzle(c, expand!(y2024::day2::part2), 459);
    bench_puzzle(c, expand!(y2024::day3::part1), 165225049);
    bench_puzzle(c, expand!(y2024::day3::part2), 108830766);
    bench_puzzle(c, expand!(y2024::day4::part1), 2642);
    bench_puzzle(c, expand!(y2024::day4::part2), 1974);
    bench_puzzle(c, expand!(y2024::day5::part1), 4790);
    bench_puzzle(c, expand!(y2024::day6::part1), 5030);
    bench_puzzle(c, expand!(y2024::day6::part2), 1928);
    bench_puzzle(c, expand!(y2024::day7::part1), 1260333054159);
    bench_puzzle(c, expand!(y2024::day7::part2), 162042343638683);
    bench_puzzle(c, expand!(y2024::day8::part1), 249);
    bench_puzzle(c, expand!(y2024::day8::part2), 905);
    bench_puzzle(c, expand!(y2024::day9::part1), 6349606724455);
    bench_puzzle(c, expand!(y2024::day9::part2), 6376648986651);
    bench_puzzle(c, expand!(y2024::day10::part1), 674);
    bench_puzzle(c, expand!(y2024::day10::part2), 1372);
    bench_puzzle(c, expand!(y2024::day11::part1), 199753);
    bench_puzzle(c, expand!(y2024::day12::part1), 1533024);
    bench_puzzle(c, expand!(y2024::day12::part2), 910066);
    bench_puzzle(c, expand!(y2024::day13::part1), 26599);
    bench_puzzle(c, expand!(y2024::day13::part2), 106228669504887);
    bench_puzzle(c, expand!(y2024::day14::part1), 230436441);
    bench_puzzle(c, expand!(y2024::day14::part2), 8270);
    bench_puzzle(c, expand!(y2024::day15::part1), 1412971);
    bench_puzzle(c, expand!(y2024::day15::part2), 1429299);
    bench_puzzle(c, expand!(y2024::day16::part1), 85396);
    bench_puzzle(c, expand!(y2024::day16::part2), 428);
    bench_puzzle(c, expand!(y2024::day17::part1), "1,5,7,4,1,6,0,3,0");
    bench_puzzle(c, expand!(y2024::day18::part1), 454);
    bench_puzzle(c, expand!(y2024::day18::part2), "8,51");
    bench_puzzle(c, expand!(y2024::day19::part1), 353);
    bench_puzzle(c, expand!(y2024::day19::part2), 880877787214477);
}

/// Benchmark a puzzle using the full input, which we load from file
fn bench_puzzle<Output, Expected>(
    c: &mut Criterion,
    (func, name): (fn(&str) -> Output, &str),
    expected: Expected,
) where
    Output: Debug + PartialEq<Expected>,
    Expected: Debug,
{
    let (year, day, part) = split_path(name);
    let input = utils::load_puzzle_input(&format!("{year}/{day}"));
    c.bench_function(&format!("puzzle/{year}/{day}/{part}"), |b| {
        b.iter(|| {
            let result = func(&input);
            assert_eq!(result, expected);
        });
    });
}

criterion_group!(benches, bench_puzzles);
criterion_main!(benches);
