use std::collections::HashMap;

use regex::Regex;

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
    let digit_map = HashMap::from([
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
        digits = ...;
        result += ...;
    }
    return result.to_string();
}

fn regex_magic(s: &str) -> Vec<&str> {
    let rx = Regex::new("one|two|three|four|five|six|seven|eight|nine|[1-9]").unwrap();
    let matches =Vec::<&str>::from([]);
    for ii in 0..s.len() {
        let substr = &s[ii..]; // todo: why do I need to borrow here?
        match = rx.find(substr); 
        if match {
            matches.append(match.group());
        }
    }
    return matches;
}
