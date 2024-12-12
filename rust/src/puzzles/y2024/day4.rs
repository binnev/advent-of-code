pub fn part1(input: &str) -> String {
    format!("{}", search(input, "XMAS"))
}

pub fn part2(input: &str) -> String {
    "".into()
}

/// Search a multiline haystack for a needle
fn search(haystack: &str, needle: &str) -> usize {
    let mut count = 0;
    let vectors = get_vectors(haystack);
    for vector in vectors {
        count += search_1d(&vector, needle);
        let reversed: String = vector.chars().rev().collect();
        count += search_1d(&reversed, needle);
    }
    count
}
/// Get the left/right, up/down, diagonal vectors for searching
fn get_vectors(input: &str) -> Vec<String> {
    let mut out = vec![];
    let lines: Vec<String> = input
        .lines()
        .map(|s| s.to_owned())
        .collect();
    let height = lines.len();
    if height == 0 {
        return vec![];
    }
    let width = lines[0].len();

    // horizontal
    for line in lines.iter() {
        out.push(line.clone());
    }
    // vertical
    for x in 0..width {
        let column: String = lines
            .iter()
            .map(|line| line.chars().nth(x).unwrap())
            .collect();
        out.push(column.clone());
    }

    // diagonal up
    //     0 1 2 3
    //   +--------
    // 0 | 0 1 2 3
    // 1 | 1 2 3 4
    // 2 | 2 3 4 5
    // 3 | 3 4 5 6
    // 4 | 4 5 6 7
    //
    // diagonal down
    //     0 1 2 3
    //   +--------
    // 0 | 4 5 6 7
    // 1 | 3 4 5 6
    // 2 | 2 3 4 5
    // 3 | 1 2 3 4
    // 4 | 0 1 2 3
    //
    for idx in 0..(height + width - 1) {
        let mut diag_up = String::new();
        let mut diag_down = String::new();
        for (y, row) in lines.iter().enumerate() {
            for (x, char) in row.chars().enumerate() {
                if y + x == idx {
                    diag_up.push(char);
                }
                if x + (height - y - 1) == idx {
                    diag_down.push(char);
                }
            }
        }
        out.push(diag_up);
        out.push(diag_down);
    }
    out
}
/// Count the occurrences of `needle` in 1d `haystack`
fn search_1d(haystack: &str, needle: &str) -> usize {
    return haystack.matches(needle).count();
}
const EXAMPLE: &str = "MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX";

#[cfg(test)]
mod tests {
    use std::collections::HashSet;

    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), "18");
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), "");
    }

    #[test]
    fn test_search_1d() {
        assert_eq!(search_1d("x", "xmas"), 0);
        assert_eq!(search_1d("xmas", "xmas"), 1);
        assert_eq!(search_1d("xmasxmas", "xmas"), 2);
        assert_eq!(search_1d("...xmas...", "xmas"), 1);
        assert_eq!(search_1d("...xmas", "xmas"), 1);
        assert_eq!(search_1d("xmas...", "xmas"), 1);
    }

    #[test]
    fn test_get_vectors() {
        let input = "
abc
def
ghi
jkl"
        .trim();
        let mut vectors = HashSet::new();
        for vector in get_vectors(input) {
            vectors.insert(vector);
        }
        assert_eq!(
            vectors,
            HashSet::from_iter(
                [
                    "abc", "def", "ghi", "jkl", // horizontal
                    "adgj", "behk", "cfil", // vertical
                    "a", "bd", "ceg", "fhj", "ik", "l", // diagonal up
                    "j", "gk", "dhl", "aei", "bf", "c", // diagonal down
                ]
                .into_iter()
                .map(|s| s.to_owned())
            ),
        );
    }
    #[test]
    fn test_get_vectors2() {
        let input = "
abcd
efgh
ijkl"
            .trim();
        let mut vectors = HashSet::new();
        for vector in get_vectors(input) {
            vectors.insert(vector);
        }
        assert_eq!(
            vectors,
            HashSet::from_iter(
                [
                    "abcd", "efgh", "ijkl", // horizontal
                    "aei", "bfj", "cgk", "dhl", // vertical
                    "a", "be", "cfi", "dgj", "hk", "l", // diagonal up
                    "i", "ej", "afk", "bgl", "ch", "d", // diagonal down
                ]
                .into_iter()
                .map(|s| s.to_owned())
            ),
        );
    }
}
