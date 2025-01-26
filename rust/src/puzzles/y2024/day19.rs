use std::collections::HashSet;

pub fn part1(input: &str) -> usize {
    let (available_parts, desired_patterns) = parse(input).unwrap();
    let mut out = 0;
    for desired in desired_patterns {
        if has_solutions(desired, &available_parts) {
            out += 1;
        }
    }
    out
}
pub fn part2(input: &str) -> usize {
    let (available_parts, desired_patterns) = parse(input).unwrap();
    let mut out = 0;
    for desired in desired_patterns {
        let solutions = get_solutions(desired, &available_parts);
        out += solutions.len();
    }
    out
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
fn get_solutions<'a, 'd>(
    desired: &'d str,
    available_parts: &Vec<&'a str>,
) -> HashSet<Vec<&'a str>> {
    println!("\nFinding solutions for {desired}\n");
    let start = PotentialSolution {
        remainder: desired,
        parts:     vec![],
    };
    let mut potential_solutions = HashSet::from([start]);
    let mut solutions = HashSet::new(); // completed solutions
    while potential_solutions.len() > 0 {
        println!("potential solutions:");
        for s in potential_solutions.iter() {
            println!("{:?}", s.parts);
        }
        if potential_solutions.len() > 10 {
            break;
        }
        let mut continue_investigating = HashSet::new();
        for solution in potential_solutions.iter() {
            for part in available_parts {
                // If one of the available parts can be subtracted from the
                // start of the desired pattern
                if let Some(trimmed) = solution.remainder.strip_prefix(part) {
                    let mut new_solution = solution.clone();
                    new_solution.remainder = trimmed;
                    new_solution.parts.push(part);
                    // If we've found a complete solution, add it to the output.
                    // If there is still some of the pattern left, continue
                    // investigating.
                    if trimmed.len() == 0 {
                        solutions.insert(new_solution);
                    } else {
                        continue_investigating.insert(new_solution);
                    }
                }
            }
            // If we get here then none of the parts matched, so the solution is
            // not viable and it is dropped.
        }
        potential_solutions = continue_investigating;
    }
    solutions
        .into_iter()
        .map(|solution| solution.parts)
        .collect()
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
        assert_eq!(
            get_solutions(desired, &available_parts),
            HashSet::from([vec!["br", "r"], vec!["b", "r", "r"],]),
        );
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
