use regex::Regex;
use std::collections::HashMap;

pub fn part1(input: &str) -> String {
    let rx = Regex::new("\\d").unwrap();
    let mut result = 0;
    for line in input.lines() {
        let digits: Vec<&str> = rx
            .find_iter(line)
            .map(|digit| digit.as_str())
            .collect();
        result += format!("{}{}", digits[0], digits[digits.len() - 1])
            .parse::<i32>()
            .unwrap();
    }
    return result.to_string();
}

pub fn part2(input: &str) -> String {
    let digit_map = HashMap::<&str, &str>::from([
        ("one", "1"),
        ("two", "2"),
        ("three", "3"),
        ("four", "4"),
        ("five", "5"),
        ("six", "6"),
        ("seven", "7"),
        ("eight", "8"),
        ("nine", "9"),
    ]);
    let mut result = 0;
    for line in input.lines() {
        let digits: Vec<&str> = regex_magic(line)
            .iter()
            .map(|m| digit_map.get(m).unwrap_or(m).to_owned())
            .collect();
        let left = digits[0];
        let right = digits[digits.len() - 1];
        result += format!("{left}{right}")
            .parse::<i32>()
            .unwrap();
    }
    return result.to_string();
}

fn regex_magic(s: &str) -> Vec<&str> {
    let rx = Regex::new("^one|two|three|four|five|six|seven|eight|nine|[1-9]")
        .unwrap();
    let mut matches = Vec::<&str>::from([]);
    for ii in 0..s.len() {
        let substr = &s[ii..]; // todo: why do I need to borrow here?
        match rx.find(substr) {
            Some(found) => {
                if found.start() != 0 {
                    continue; // for some reason the regex ignores my "^"!!
                }
                let match_str = found.as_str();
                matches.push(match_str);
            }
            None => {} // no need to panik
        }
    }
    return matches;
}

pub const EXAMPLE1: &str = "1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet";

pub const EXAMPLE2: &str = "two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen";

#[cfg(test)]
mod tests {
    use crate::puzzles::y2023::day1::*;
    use test_case::test_case;

    #[test_case("1two", vec!["1", "two"])]
    #[test_case("oneight", vec!["one", "eight"])]
    #[test_case("nineight", vec!["nine", "eight"])]
    #[test_case("twone", vec!["two", "one"])]
    #[test_case("twoneight", vec!["two", "one", "eight"])]
    fn test_regex_magic(s: &str, expected: Vec<&str>) {
        assert_eq!(regex_magic(s), expected);
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(&EXAMPLE1), "142");
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE2), "281");
    }
}
