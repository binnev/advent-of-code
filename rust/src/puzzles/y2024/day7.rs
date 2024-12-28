/// Get the sum of the checksums for the equations that can be true
pub fn part1(input: &str) -> String {
    let equations = parse(input);
    let mut out = 0;
    for equation in equations {
        if brute_force(equation.checksum, equation.numbers) {
            out += equation.checksum;
        }
    }
    format!("{out}")
}
pub fn part2(input: &str) -> String {
    "".into()
}
const EXAMPLE: &str = "190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20";

struct Equation {
    numbers:  Vec<usize>,
    checksum: usize,
}

/// Try every combination. Will scale terribly.
fn brute_force(checksum: usize, numbers: Vec<usize>) -> bool {
    let numbers = numbers.into_iter().rev().collect();
    let combos = get_all_combinations(numbers);
    for result in combos {
        if result == checksum {
            return true;
        }
    }
    false
}

fn get_all_combinations(numbers: Vec<usize>) -> Vec<usize> {
    let mut out = vec![];
    if numbers.len() == 2 {
        // base case
        let left = numbers[0];
        let right = numbers[1];
        out.push(left + right);
        out.push(left * right);
    } else {
        // recursive case
        let left = numbers[0];
        let rest = numbers[1..].to_vec();
        for right in get_all_combinations(rest) {
            out.push(left + right);
            out.push(left * right);
        }
    }
    out
}
/// Return true if it is possible to substitute in a combination of operators
/// such that the equation evaluates to the checksum
fn try_evaluate(checksum: usize, numbers: Vec<usize>) -> bool {
    // base case -- 2 numbers
    if numbers.len() == 2 {
        let left = numbers[0];
        let right = numbers[1];
        return left + right == checksum || left * right == checksum;
    }

    // recursive case -- >2 numbers
    let left = numbers[0];
    let rest = numbers[1..].to_vec().clone();
    // addition: left + ... == checksum
    // same as
    // ... = checksum - left
    let new_checksum = checksum - left;
    if try_evaluate(new_checksum, rest.clone()) {
        return true;
    }

    // multiplication: left * ...
    // same as
    // ... = checksum / left
    let new_checksum = checksum / left; // this might be buggy rounding down
    if try_evaluate(new_checksum, rest) {
        return true;
    }

    false
}

fn parse(input: &str) -> Vec<Equation> {
    let mut out = vec![];
    for line in input.lines() {
        let mut parts = line.split(": ");
        let checksum = parts.next().unwrap().parse().unwrap(); // yolo
        let numbers = parts
            .next()
            .unwrap()
            .split(" ")
            .map(|s| s.parse().unwrap())
            .collect();
        let equation = Equation { checksum, numbers };
        out.push(equation);
    }
    out
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), "3749");
    }
    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), "");
    }

    #[test]
    fn test_brute_force() {
        assert!(brute_force(190, vec![10, 19]));
        assert!(brute_force(292, vec![11, 6, 16, 20]));
        assert!(brute_force(3267, vec![81, 40, 27]));
        assert!(!brute_force(21037, vec![9, 7, 18, 13]));
    }
}
