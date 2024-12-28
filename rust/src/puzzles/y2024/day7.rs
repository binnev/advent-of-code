/// Get the sum of the checksums for the equations that can be true
pub fn part1(input: &str) -> String {
    let equations = parse(input);
    let out = sum_possible_equations(equations, &vec![SUB, DIV]);
    format!("{out}")
}
/// Same as part 1, but we add another operator
pub fn part2(input: &str) -> String {
    let equations = parse(input);
    let out = sum_possible_equations(equations, &vec![SUB, DIV, STRIP]);
    format!("{out}")
}

fn sum_possible_equations(
    equations: Vec<Equation>,
    operators: &Vec<fn(usize, usize) -> Option<usize>>,
) -> usize {
    let mut out = 0;
    for equation in equations {
        if modify_the_checksum(equation.checksum, equation.numbers, &operators)
        {
            out += equation.checksum;
        }
    }
    out
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
fn try_every_combination(
    checksum: usize,
    numbers: Vec<usize>,
    operators: &Vec<fn(usize, usize) -> usize>,
) -> bool {
    let mut results = vec![];
    let mut numbers = numbers;
    results.push(numbers.remove(0));
    for number in numbers {
        let mut new_results = vec![];
        for result in results {
            for operator in operators {
                new_results.push(operator(result, number))
            }
        }
        results = new_results;
    }

    results.iter().any(|&r| r == checksum)
}

/// Modify the checksum as we proceed from left to right. This can early exit.
/// For example:
///
/// 100: 3 2 20
///
/// Can only be solved by 3 + 2 * 20.
/// (3 + 2) * 20 = 100
/// 3 + 2 = 100 / 20 = 5  // check 100 % 20 == 0
/// 3 = 5 - 2 = 3         // check 5 - 2 > 0
/// 3 = 3                 // final number should equal itself
///
/// So we go from right to left, and apply the inverse operations to the
/// checksum
///
/// forward         backward
/// 2 + 3 = 5       5 - 3 = 2
/// 2 * 3 = 6       6 / 3 = 2
/// 2 | 3 = 23      23 ! 3 = 2
///
/// But how to handle the branching?
/// 3 ? 2 ? 20 = 100
/// 3 ? 2 = 100 ? 20
///     add: 3 ? 2 + 20 = 100 -> 3 ? 2 = 100 - 20 = 80
///     mul: 3 ? 2 * 20 = 100 -> 3 ? 2 = 100 / 20 = 5
///     cat: 3 ? 2 | 20 = 100 -> 3 ? 2 = 100 ! 20 = None (20 not in 100)
///
/// So now 3 ? 2 = [80, 5]
/// for 80:
///     add: 3 + 2 = 80 -> 80 - 2 = 78
///     mul: 3 * 2 = 80 -> 80 / 2 = 40
///     cat: 3 | 2 = 80 -> 80 ! 2 = None
/// for 5:
///     add: 3 + 2 = 5 -> 5 - 2 = 3
///     mul: 3 * 2 = 5 -> 5 / 2 = None (doesn't divide evenly)
///     cat: 3 | 2 = 5 -> 5 ! 2 = None
///
/// So now 3 = [78, 40, 3]
///
/// no more operations, so we search for 3 in the list. It's in there, so we
/// return true.
///
///
/// Compare this to the brute force approach:
/// 3 ? 2 ? 20 = 100
/// apply 3:
/// [3]
/// apply 2:
/// [
///     3 + 2,
///     3 * 2,
///     3 | 2,
/// ]
/// apply 20:
/// [
///     3 + 2 + 20,
///     3 * 2 + 20,
///     3 | 2 + 20,
///     3 + 2 * 20,
///     3 * 2 * 20,
///     3 | 2 * 20,
///     3 + 2 | 20,
///     3 * 2 | 20,
///     3 | 2 | 20,
/// ]
fn modify_the_checksum(
    checksum: usize,
    numbers: Vec<usize>,
    inverse_operators: &Vec<fn(usize, usize) -> Option<usize>>,
) -> bool {
    let mut numbers = numbers;
    let mut checksums = vec![checksum];
    while numbers.len() > 1 {
        let n = numbers.pop().unwrap();
        checksums = {
            let mut new = vec![];
            for cs in checksums.iter() {
                for op in inverse_operators {
                    if let Some(number) = op(*cs, n) {
                        new.push(number);
                    }
                }
            }
            new
        };
    }
    let n = numbers.pop().unwrap();
    checksums.contains(&n)
}

// reverse operations
const SUB: fn(usize, usize) -> Option<usize> = |a, b| a.checked_sub(b);
const DIV: fn(usize, usize) -> Option<usize> = |a, b| {
    if a % b == 0 {
        Some(a / b)
    } else {
        None
    }
};
const STRIP: fn(usize, usize) -> Option<usize> = |a, b| {
    let a = format!("{a}");
    let b = format!("{b}");
    let stripped = a.strip_suffix(&b)?;
    stripped.parse().ok()
};

const ADD: fn(usize, usize) -> usize = |a, b| a + b;
const MUL: fn(usize, usize) -> usize = |a, b| a * b;
const CAT: fn(usize, usize) -> usize =
    |a, b| format!("{a}{b}").parse().unwrap();

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
        assert_eq!(part2(EXAMPLE), "11387");
    }

    #[test]
    fn test_brute_force() {
        let operators = [ADD, MUL].to_vec();
        assert!(try_every_combination(190, vec![10, 19], &operators));
        assert!(try_every_combination(292, vec![11, 6, 16, 20], &operators));
        assert!(try_every_combination(3267, vec![81, 40, 27], &operators));
        assert!(!try_every_combination(
            21037,
            vec![9, 7, 18, 13],
            &operators
        ));

        let operators = [ADD, MUL, CAT].to_vec();
        assert!(try_every_combination(156, vec![15, 6], &operators));
        assert!(try_every_combination(7290, vec![6, 8, 6, 15], &operators));
        assert!(try_every_combination(192, vec![17, 8, 14], &operators));
    }
    #[test]
    fn test_modify_checksum() {
        let operators = [SUB, DIV].to_vec();
        assert!(modify_the_checksum(190, vec![10, 19], &operators));
        assert!(modify_the_checksum(292, vec![11, 6, 16, 20], &operators));
        assert!(modify_the_checksum(3267, vec![81, 40, 27], &operators));
        assert!(!modify_the_checksum(21037, vec![9, 7, 18, 13], &operators));

        let operators = [SUB, DIV, STRIP].to_vec();
        assert!(modify_the_checksum(156, vec![15, 6], &operators));
        assert!(modify_the_checksum(7290, vec![6, 8, 6, 15], &operators));
        assert!(modify_the_checksum(192, vec![17, 8, 14], &operators));
    }
    #[test]
    fn test_modify_checksum_panic() {
        let operators = [SUB, DIV, STRIP].to_vec();
        // should not panic
        // 12763566858: [1, 6, 641, 895, 618, 83, 6]
        modify_the_checksum(
            12763566858,
            vec![1, 6, 641, 895, 618, 83, 6],
            &operators,
        );
    }
}
