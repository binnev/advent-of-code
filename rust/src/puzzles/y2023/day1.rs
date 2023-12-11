use regex::Regex;

pub fn part1(input: &str) -> String {
    let rx = Regex::new("\\d").unwrap();
    let mut result = 0;
    for line in input.lines() {
        let digits: Vec<&str> =
            rx.find_iter(line).map(|digit| digit.as_str()).collect();
        // struggling to concatenate two strings here
        let mut new_digit = digits[0].to_owned();
        new_digit.push_str(digits[digits.len() - 1]);
        result += new_digit.parse::<i32>().unwrap();
    }
    return result.to_string();
}
