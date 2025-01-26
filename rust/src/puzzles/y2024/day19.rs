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
    0
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
fn get_num_solutions(desired: &str, available_parts: &Vec<&str>) -> usize {
    // Base case: there is nothing left to construct, so we were able to
    // construct the desired pattern
    if desired.len() == 0 {
        return 1;
    }

    // Recursive case: there are letters left in the desired pattern. There may
    // be multiple parts that match the start of the pattern. Loop over the
    // available parts and see which ones match the start of the desired
    // pattern. For those that match, subtract them from the desired pattern
    // and investigate recursively
    let matching_parts: Vec<_> = available_parts
        .into_iter()
        .filter(|&part| desired.starts_with(part))
        .collect();
    let mut solutions = 0;
    for part in matching_parts {
        let trimmed = desired.trim_start_matches(part);
        solutions += get_num_solutions(trimmed, available_parts);
    }
    solutions
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
        assert_eq!(part2(EXAMPLE), 0);
    }

    #[test]
    fn test_get_num_solutions() {
        let desired = "brr";
        let available_parts = vec!["br", "b", "r"];
        // [br, r] and [b, r, r] are both possible.
        assert_eq!(get_num_solutions(desired, &available_parts), 2,);
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
