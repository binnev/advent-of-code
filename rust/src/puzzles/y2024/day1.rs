pub fn part1(input: &str) -> String {
    let (mut left_list, mut right_list) = parsing(input);
    left_list.sort();
    right_list.sort();
    let out: usize = left_list
        .iter()
        .zip(right_list)
        .map(|(l, r)| l.abs_diff(r))
        .sum();
    format!("{out}")
}

pub fn part2(input: &str) -> String {
    let (left, right) = parsing(input);
    let out: usize = left.into_iter().map(|l| l * count(&right, l)).sum();
    format!("{out}")
}

fn count(haystack: &Vec<usize>, needle: usize) -> usize {
    haystack.iter().filter(|&&item| item == needle).count()
}

fn parsing(input: &str) -> (Vec<usize>, Vec<usize>) {
    let mut left_list = vec![];
    let mut right_list = vec![];
    for line in input.lines() {
        let mut chars = line.split_ascii_whitespace();
        let (left, right) = chars.next().zip(chars.next()).unwrap();
        let left: usize = left.parse().unwrap();
        let right: usize = right.parse().unwrap();
        left_list.push(left);
        right_list.push(right);
    }
    (left_list, right_list)
}
const EXAMPLE: &str = "3   4
4   3
2   5
1   3
3   9
3   3";

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), "11");
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), "31");
    }
}
