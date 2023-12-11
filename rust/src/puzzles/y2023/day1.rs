use regex::Regex;

pub fn part1(input: &str) -> String {
    let rx = Regex::new("\\d").unwrap();
    let mut result = 0;
    for line in input.lines() {
        let matches: Vec<&str> =
            rx.find_iter(line).map(|m| m.as_str()).collect();
        print!("{:?}", matches);
        // let matches = rx.captures(line).unwrap();
        // let first: i32 = matches[0].parse().unwrap();
        // let last: i32 = matches[matches.len() - 1].parse().unwrap();
        // print!("matches={:?}, ", matches);
        // println!("first={first}, last={last}, line={line}");
        // result = result + first + last;
    }
    return result.to_string();
}

fn hello() -> String {
    return String::from("Hello");
}

#[cfg(test)]
mod tests {
    // this makes load_puzzle_input, greet available in the current scope
    // without the absolute path prefix
    use super::*;

    #[test]
    fn test_hello() {
        let result = hello();
        let expected = String::from("Hello");
        assert_eq!(result, expected);
    }
}
