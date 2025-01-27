pub fn part1(input: &str) -> usize {
    let reports = parse(input);
    reports
        .into_iter()
        .filter(|report| is_safe_tolerant(report, false))
        .count()
}

pub fn part2(input: &str) -> usize {
    let reports = parse(input);
    reports
        .into_iter()
        .filter(|report| is_safe_tolerant(report, true))
        .count()
}
/// Calculate if the report is safe without any fault tolerance
fn is_safe(report: &Vec<usize>) -> bool {
    let mut increasing: Option<bool> = None;
    let mut iter = report.iter();
    let mut left = iter.next().unwrap();
    while let Some(right) = iter.next() {
        let diff = right.abs_diff(*left);
        // the first 2 elements set the direction
        if increasing.is_none() {
            increasing = Some(right > left);
        }
        if diff < 1 || diff > 3 || Some(right > left) != increasing {
            return false;
        }
        left = right;
    }
    true
}
/// Calculate if the report is safe, possibly tolerating 1 fault
fn is_safe_tolerant(report: &Vec<usize>, tolerance: bool) -> bool {
    is_safe(report) // if is safe, return early
        || (tolerance // else, if tolerance, see if removing any element works
            && remove_every_element(report.clone())
                .into_iter()
                .any(|rep| is_safe(&rep)))
}
fn remove_every_element(v: Vec<usize>) -> Vec<Vec<usize>> {
    let mut out = vec![];
    for idx in 0..v.len() {
        out.push(remove(v.clone(), idx));
    }
    out
}
fn remove(v: Vec<usize>, idx: usize) -> Vec<usize> {
    let mut v = v;
    v.remove(idx);
    v
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

pub const EXAMPLE: &str = "7 6 4 2 1
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
        assert_eq!(part1(EXAMPLE), 2);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 4);
    }

    #[test]
    fn test_is_safe() {
        assert_eq!(is_safe_tolerant(&vec![7, 6, 4, 2, 1], false), true); // Safe because the levels are all decreasing by 1 or 2.
        assert_eq!(is_safe_tolerant(&vec![1, 2, 7, 8, 9], false), false); // Unsafe because 2 7 is an increase of 5.
        assert_eq!(is_safe_tolerant(&vec![9, 7, 6, 2, 1], false), false); // Unsafe because 6 2 is a decrease of 4.
        assert_eq!(is_safe_tolerant(&vec![1, 3, 2, 4, 5], false), false); // Unsafe because 1 3 is increasing but 3 2 is decreasing.
        assert_eq!(is_safe_tolerant(&vec![8, 6, 4, 4, 1], false), false); // Unsafe because 4 4 is neither an increase or a decrease.
        assert_eq!(is_safe_tolerant(&vec![1, 3, 6, 7, 9], false), true); // Safe because the levels are all increasing by 1, 2, or 3

        // and now tolerating 1 bad level
        assert_eq!(is_safe_tolerant(&vec![7, 6, 4, 2, 1], true), true); // Safe without removing any level.
        assert_eq!(is_safe_tolerant(&vec![1, 2, 7, 8, 9], true), false); // Unsafe regardless of which level is removed.
        assert_eq!(is_safe_tolerant(&vec![9, 7, 6, 2, 1], true), false); // Unsafe regardless of which level is removed.
        assert_eq!(is_safe_tolerant(&vec![1, 3, 2, 4, 5], true), true); // Safe by removing the second level, 3.
        assert_eq!(is_safe_tolerant(&vec![8, 6, 4, 4, 1], true), true); // Safe by removing the third level, 4.
        assert_eq!(is_safe_tolerant(&vec![1, 3, 6, 7, 9], true), true); // Safe without removing any level.

        // custom cases
        assert_eq!(is_safe_tolerant(&vec![1, 2, 3, 4, 5], true), true); // Safe without any modifications
        assert_eq!(is_safe_tolerant(&vec![999, 1, 2, 3, 4], true), true); // first value diff too big
        assert_eq!(is_safe_tolerant(&vec![1, 999, 3, 4, 5], true), true); // Safe because we can remove 999
        assert_eq!(is_safe_tolerant(&vec![1, 3, 999, 4, 5], true), true); // Safe because we can remove 999
        assert_eq!(is_safe_tolerant(&vec![1, 3, 4, 999, 5], true), true); // Safe because we can remove 999
        assert_eq!(is_safe_tolerant(&vec![1, 3, 4, 5, 999], true), true); // Safe because we can remove 999
        assert_eq!(is_safe_tolerant(&vec![1, 3, 4, 3, 999], true), false); // Unsafe; changes direction after removing 999
        assert_eq!(is_safe_tolerant(&vec![1, 3, 0, 6, 9], true), true); // Safe if we remove the 0

        // This is the crux. This one is safe if we remove the first element.
        // But the transition from element 0 to 1 does not raise an error, so 0
        // is never considered for removal...
        assert_eq!(is_safe_tolerant(&vec![3, 1, 3, 6, 9], true), true); // first value direction change

        ()
    }
}
