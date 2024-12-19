pub fn part1(input: &str) -> String {
    format!("{}", search(input, "XMAS"))
}

/// Search for X-MAS the right way up, and rotate the text grid
pub fn part2(input: &str) -> String {
    let mut grid = input.to_owned();
    let mut count = 0;
    for _ in 0..4 {
        count += count_xmas(&grid);
        grid = rotate_grid_90_clockwise(&grid);
    }
    format!("{count}")
}

/// Count the number of X-MAS in the grid.
fn count_xmas(haystack: &str) -> usize {
    let mut count = 0;
    for (y, line) in haystack.lines().enumerate() {
        for x in 0..line.len() {
            let xy = (x as i32, y as i32); // risky cast but whatever
            if search_xmas_here(haystack, xy) {
                count += 1;
            }
        }
    }
    count
}

/// Return true if there is an X-MAS, with the 'A' centered on 'xy'
/// "X-MAS" here means "an X of MAS":
///
///     M.S
///     .A.
///     M.S
fn search_xmas_here(haystack: &str, xy: (i32, i32)) -> bool {
    let (x, y) = xy;
    let top_left = (x - 1, y - 1);
    let top_right = (x + 1, y - 1);
    let btm_left = (x - 1, y + 1);
    let btm_right = (x + 1, y + 1);
    let grid: Vec<String> = haystack
        .lines()
        .map(|line| line.to_owned())
        .collect();

    _get(&grid, xy) == Some('A')
        && _get(&grid, top_left) == Some('M')
        && _get(&grid, btm_left) == Some('M')
        && _get(&grid, top_right) == Some('S')
        && _get(&grid, btm_right) == Some('S')
}

fn _get(grid: &Vec<String>, xy: (i32, i32)) -> Option<char> {
    let x: usize = match xy.0.try_into() {
        Ok(x) => Some(x),
        Err(_) => None,
    }?;
    let y: usize = match xy.1.try_into() {
        Ok(x) => Some(x),
        Err(_) => None,
    }?;

    grid.get(y)
        .and_then(|s| s.chars().nth(x))
}

/// Search a multiline haystack for a needle by getting all the vectors -- rows,
/// columns, diagonals -- and searching for the string in all of them.
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
/// Get the rows, columns, and diagonals for searching
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

/// thanks ChatGPT
fn rotate_grid_90_clockwise(grid: &str) -> String {
    let grid: Vec<_> = grid.lines().collect();
    let num_rows = grid.len();
    let num_cols = grid[0].len();

    let mut rotated_grid = vec![String::new(); num_cols];

    for col in 0..num_cols {
        for row in (0..num_rows).rev() {
            rotated_grid[col].push(grid[row].chars().nth(col).unwrap());
        }
    }

    rotated_grid.join("\n")
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
        assert_eq!(part2(EXAMPLE), "9");
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

    #[test]
    fn test_search_xmas_here() {
        let s = "
M.S
.A.
M.S
"
        .trim();

        assert_eq!(search_xmas_here(s, (0, 0)), false);
        assert_eq!(search_xmas_here(s, (1, 1)), true);
        assert_eq!(search_xmas_here(s, (2, 2)), false);
    }

    #[test]
    fn test_rotate() {
        let input = "
abc
def
ghi"
        .trim();
        let expected = "
gda
heb
ifc"
        .trim();
        assert_eq!(rotate_grid_90_clockwise(input), expected);
    }
}
