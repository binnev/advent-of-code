use std::collections::HashMap;

// Sum the middle page of every correctly ordered list of pages
pub fn part1(input: &str) -> usize {
    let mut out = 0;
    let (rules, page_lists) = parse(input);
    for pages in page_lists.into_iter() {
        let index = index_pages(pages.clone());
        if check_rules(&index, &rules) {
            let middle_page = pages[pages.len() / 2];
            out += middle_page;
        }
    }
    out
}
pub fn part2(input: &str) -> usize {
    0
}
pub const EXAMPLE: &str = "47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47";

/// The first page must appear before the last page
struct Rule {
    first_page: usize,
    last_page:  usize,
}
type Page = usize;

fn check_rules(index: &HashMap<Page, usize>, rules: &Vec<Rule>) -> bool {
    rules
        .iter()
        .all(|rule| check_rule(index, rule)) // should fail fast
}
fn check_rule(index: &HashMap<Page, usize>, rule: &Rule) -> bool {
    index
        .get(&rule.first_page)
        .zip(index.get(&rule.last_page))
        // first page must come before last page, meaning that the first
        // position must be less than the last position
        .map(|(first_pos, last_pos)| first_pos < last_pos)
        // if either page is not in the index, ignore the rule (assume it is
        // satisfied, so true)
        .unwrap_or(true)
}
/// Calculate the position of each page once, for quick repeated lookups later.
/// Otherwise we'll be spamming `pages.iter().position(...)` all over the place
fn index_pages(pages: Vec<Page>) -> HashMap<Page, usize> {
    let mut index = HashMap::new();
    for (position, page) in pages.into_iter().enumerate() {
        index.insert(page, position);
    }
    index
}
fn parse(input: &str) -> (Vec<Rule>, Vec<Vec<Page>>) {
    let mut parts = input.split("\n\n");
    let rules_strings = parts.next().unwrap().trim();
    let pages_strings = parts.next().unwrap().trim();
    let rules = rules_strings
        .split("\n")
        .map(parse_rule)
        .collect();
    let pages = pages_strings
        .split("\n")
        .map(parse_pages)
        .collect();
    (rules, pages)
}

fn parse_pages(s: &str) -> Vec<Page> {
    s.split(",")
        .map(|page| page.parse().unwrap())
        .collect()
}
fn parse_rule(s: &str) -> Rule {
    let mut parts = s.split("|");
    let first: usize = parts.next().unwrap().parse().unwrap();
    let last: usize = parts.next().unwrap().parse().unwrap();
    Rule {
        first_page: first,
        last_page:  last,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 143);
    }
    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 0);
    }
}
