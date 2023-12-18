use regex::Regex;
use std::collections::HashMap;

pub fn part1(input: &str) -> String {
    let rx = Regex::new("\\d").unwrap();
    let mut result = 0;
    for line in input.lines() {
        let digits: Vec<&str> =
            rx.find_iter(line).map(|digit| digit.as_str()).collect();
        // struggling to concatenate two strings here
        result += (digits[0].to_owned() + digits[digits.len() - 1])
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
        let digit_strings = regex_magic(line);
        let digits: Vec<&str> = digit_strings
            .iter()
            .map(|d| digit_map.get(d).or_else(|| Some(d)).unwrap())
            .collect();
        // result += (digits[0].to_owned() + digits[digits.len() - 1])
        //     .parse::<i32>()
        //     .unwrap()
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
                let match_str = found.as_str();
                matches.push(match_str);
            }
            None => {} // no need to panik
        }
    }
    return matches;
}

#[cfg(test)]
mod tests {
    use crate::puzzles::y2023::day1::*;
    use crate::utils;
    use test_case::test_case;

    #[test_case("1two", vec!["1", "two"])]
    #[test_case("oneight", vec!["one", "eight"])]
    #[test_case("nineight", vec!["nine", "eight"])]
    #[test_case("twone", vec!["two", "one"])]
    fn test_regex_magic(s: &str, expected: Vec<&str>) {
        assert_eq!(regex_magic(s), expected);
    }

    // todo: getting weird double hits on the last match

    #[test]
    fn test_part1() {
        let input = utils::load_puzzle_input("2023/day1");
        let result = part1(&input);
        let expected = "55123";
        assert_eq!(result, expected);
    }
}
