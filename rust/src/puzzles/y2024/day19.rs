use std::collections::{HashMap, HashSet};

pub fn part1(input: &str) -> usize {
    let (available_parts, desired_patterns) = parse(input).unwrap();
    desired_patterns
        .into_iter()
        .filter(|desired| has_solutions(desired, &available_parts))
        .count()
}
pub fn part2(input: &str) -> usize {
    let (available_parts, desired_patterns) = parse(input).unwrap();
    desired_patterns
        .into_iter()
        .map(|desired| get_num_solutions(desired, &available_parts))
        .sum()
}
fn has_solutions(desired: &str, available_parts: &Vec<&str>) -> bool {
    let mut options = HashSet::from([desired]);
    while options.len() > 0 {
        let mut new_options = HashSet::new();
        // E.g. pattern might be "rrb"
        for pattern in options {
            // e.g. part might be "r"
            for part in available_parts {
                if pattern.starts_with(part) {
                    // e.g. trimmed might be "rb"
                    let trimmed = pattern.trim_start_matches(part);
                    // if the trimmed pattern is len 0, that means that all of
                    // its characters were trimmed using the
                    // available parts. I.e. the desired pattern
                    // can be constructed using the available parts.
                    if trimmed.len() == 0 {
                        return true;
                    }
                    new_options.insert(trimmed);
                }
            }
        }
        options = new_options;
    }
    false
}
/// Find the number of ways the desired pattern can be constructed from the
/// available parts.
///
/// This works by iterating over the available parts and trying to subtract them
/// from the start of the desired pattern. This continues until either
/// - no parts can be subtracted (fail)
/// - the whole desired pattern is consumed (success)
///
/// Because multiple parts could match at each stage, we keep a hashset of all
/// the viable solutions. The hashset enforces uniqueness which keeps this
/// relatively quick.
///
/// OK so the hashset does not keep it quick at all.
/// Ideas to make this better:
/// - Use a Trie?
///
/// Instead of storing all the parts that make a solution, store the
/// combination of parts as a string, along with the _number of ways it can be
/// created_.
///
/// So instead of:
///
/// {
///     ["w", "w", "gg"],
///     ["ww", "gg"],
/// }
///
/// do
///
/// {
///     "wwgg": 2
/// }
///
/// We don't need to actually give the solution parts, we just need the solution
/// _count_.
fn get_num_solutions<'a, 'd>(
    desired: &'d str,
    available_parts: &Vec<&'a str>,
) -> usize {
    let mut out = 0; // number of ways we can create the desired pattern
    let mut solutions: HashMap<String, usize> = HashMap::from([("".into(), 1)]);
    while solutions.len() > 0 {
        let mut new_solutions = HashMap::new();
        // e.g. ("rg", 2) because [r, g], [rg]
        // or   ("r", 1)  because [r]
        for (solution, count) in solutions {
            // e.g. "g"
            // or   "gg"
            for part in available_parts {
                // e.g. "rgg" from [r, g, g] or [rg, g]
                // or   "rgg" from [r, gg]
                let new = solution.clone() + part;
                if desired == new {
                    out += count;
                } else if desired.starts_with(&new) {
                    new_solutions
                        .entry(new)
                        .and_modify(|e| *e += count)
                        .or_insert(count);
                }
            }
        }
        solutions = new_solutions;
    }
    out
}
#[derive(PartialEq, Eq, Hash, Clone, Debug)]
struct PotentialSolution<'a, 'd> {
    remainder: &'d str,
    parts:     Vec<&'a str>,
}
fn parse(input: &str) -> Option<(Vec<&str>, Vec<&str>)> {
    let mut parts = input.split("\n\n");
    let available_parts = parts.next()?.split(", ").collect();
    let desired_patterns = parts.next()?.lines().collect();
    Some((available_parts, desired_patterns))
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 6);
    }
    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 16);
    }

    #[test]
    fn test_get_solutions() {
        let desired = "brr";
        let available_parts = vec!["br", "b", "r"];
        // [br, r] and [b, r, r] are both possible.
        assert_eq!(get_num_solutions(desired, &available_parts), 2);
    }
}
const EXAMPLE: &str = "r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb";
