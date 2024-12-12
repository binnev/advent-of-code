pub fn part1(input: &str) -> String {
    let reports = parse(input);
    let out = reports.into_iter().filter(|report| is_safe(report)).count();
    format!("{out}")
}

pub fn part2(input: &str) -> String {
    "".into()
}

fn is_safe(report: &Vec<usize>) -> bool {
    let mut increasing: Option<bool> = None;
    let mut iter = report.iter();
    let mut left = iter.next().unwrap();
    while let Some(right) = iter.next() {
        // set the direction on the first 2 elements
        if increasing.is_none() {
            increasing = Some(right > left);
        }
        let diff = right.abs_diff(*left);
        if diff < 1 || diff > 3 {
            return false;
        }
        if Some(right > left) != increasing {
            return false;
        }
        left = right;
    }
    true
}

fn parse(input: &str) -> Vec<Vec<usize>> {
    input
        .lines()
        .map(|line| {
            line.split_ascii_whitespace()
                .map(|s| s.parse().unwrap())
                .collect()
        })
        .collect()
}

const EXAMPLE: &str = "7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9";

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), "2");
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), "");
    }

    #[test]
    fn test_is_safe() {
        for (report, expected) in vec![
            (vec![7, 6, 4, 2, 1], true), // Safe because the levels are all decreasing by 1 or 2.
            (vec![1, 2, 7, 8, 9], false), // Unsafe because 2 7 is an increase of 5.
            (vec![9, 7, 6, 2, 1], false), // Unsafe because 6 2 is a decrease of 4.
            (vec![1, 3, 2, 4, 5], false), // Unsafe because 1 3 is increasing but 3 2 is decreasing.
            (vec![8, 6, 4, 4, 1], false), // Unsafe because 4 4 is neither an increase or a decrease.
            (vec![1, 3, 6, 7, 9], true), // Safe because the levels are all increasing by 1, 2, or 3
        ] {
            let result = is_safe(&report);
            assert_eq!(result, expected);
        }
    }
}
