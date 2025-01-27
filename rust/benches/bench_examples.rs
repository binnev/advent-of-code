use advent::puzzles::{y2023, y2024};
use advent::{expand, utils::split_path};
use criterion::{criterion_group, criterion_main, Criterion};
use std::fmt::Debug;

/// Benchmark all the puzzles with their example input.
/// Filter for a specific year/day/part by passing it to cargo bench e.g.:
/// cargo bench example/2024
/// cargo bench example/2024/day1
/// cargo bench example/2024/day1/part1
pub fn bench_examples(c: &mut Criterion) {
    // ----- 2023 -----
    bench_example(c, expand!(y2023::day1::part1), y2023::day1::EXAMPLE1, "142");
    bench_example(c, expand!(y2023::day1::part2), y2023::day1::EXAMPLE2, "281");

    // ----- 2024 -----
    bench_example(c, expand!(y2024::day1::part1), y2024::day1::EXAMPLE, 11);
    bench_example(c, expand!(y2024::day1::part2), y2024::day1::EXAMPLE, 31);
    bench_example(c, expand!(y2024::day2::part1), y2024::day2::EXAMPLE, 2);
    bench_example(c, expand!(y2024::day2::part2), y2024::day2::EXAMPLE, 4);
    bench_example(c, expand!(y2024::day3::part1), y2024::day3::EXAMPLE, 161);
    bench_example(c, expand!(y2024::day3::part2), y2024::day3::EXAMPLE, 48);
    bench_example(c, expand!(y2024::day19::part2), y2024::day19::EXAMPLE, 16);
}

/// Benchmark a puzzle using the example input
fn bench_example<Output, Expected>(
    c: &mut Criterion,
    (func, name): (fn(&str) -> Output, &str),
    input: &str,
    expected: Expected,
) where
    Output: Debug + PartialEq<Expected>,
    Expected: Debug,
{
    let (year, day, part) = split_path(name);
    c.bench_function(&format!("example/{year}/{day}/{part}"), |b| {
        b.iter(|| {
            let result = func(&input);
            assert_eq!(result, expected);
        });
    });
}

criterion_group!(benches, bench_examples);
criterion_main!(benches);
