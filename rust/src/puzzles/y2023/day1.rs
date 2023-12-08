use regex::Regex;

pub fn part1(input: &str) -> String {
    let rx = Regex::new("\\d").unwrap();
    let mut result = 0;
    for line in input.lines() {
        let matches = rx.captures(line).unwrap();
        let first: i32 = matches[0].parse().unwrap();
        let last: i32 = matches[matches.len() - 1].parse().unwrap();
        print!("matches={:?}, ", matches);
        println!("first={first}, last={last}, line={line}");
        result = result + first + last;
    }
    return result.to_string();
}

#[cfg(test)]
mod tests {
    use crate::utils;

    // this makes load_puzzle_input, greet available in the current scope
    // without the absolute path prefix
    use super::*;
    #[test]
    fn test_load_puzzle_input() {
        let input = utils::load_puzzle_input("2023/day1");
        let result = part1(&input);
        let expected = "55123";
        assert_eq!(result, expected);
    }
}
