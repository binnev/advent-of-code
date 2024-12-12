use regex::Regex;

pub fn part1(input: &str) -> String {
    let pairs = parse(input);
    let out: usize = pairs
        .iter()
        .map(|(left, right)| left * right)
        .sum();
    format!("{out}")
}

pub fn part2(input: &str) -> String {
    "".into()
}

fn parse(input: &str) -> Vec<(usize, usize)> {
    let rx = Regex::new(r"mul\((\d+),(\d+)\)").unwrap();
    let mut out = vec![];
    for cap in rx.captures_iter(input) {
        let left = cap
            .get(1)
            .unwrap()
            .as_str()
            .parse()
            .unwrap();
        let right = cap
            .get(2)
            .unwrap()
            .as_str()
            .parse()
            .unwrap();
        out.push((left, right));
    }
    out
}
const EXAMPLE: &str =
    "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))";

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), "161");
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), "");
    }

    #[test]
    fn test_parse() {
        assert_eq!(parse(EXAMPLE), vec![(2, 4), (5, 5), (11, 8), (8, 5)])
    }
}
