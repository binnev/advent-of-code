use std::iter::repeat;

pub fn part1(input: &str) -> String {
    let expanded = expand(input);
    let defragmented = defragment(&expanded);
    let checksum = compute_checksum(&defragmented);
    format!("{checksum}")
}
pub fn part2(input: &str) -> String {
    "".into()
}
const EXAMPLE: &str = "2333133121414131402";
fn compute_checksum(s: &str) -> usize {
    let mut out = 0;
    for (ii, ch) in s.chars().enumerate() {
        if let Some(number) = ch.to_digit(10) {
            out += number as usize * ii;
        } else {
            // Assume everything to the right is also empty
            break;
        }
    }
    out
}
fn expand(s: &str) -> String {
    let mut is_file = true;
    let mut out = String::new();
    let mut file_id = 0;
    for n_blocks in s.chars() {
        let n_blocks = n_blocks.to_digit(10).unwrap() as usize; // input is only numbers
        let ch = if is_file {
            char::from_digit(file_id as u32, 10)
                .expect("Digit is too big to turn into char!")
        } else {
            '.'
        };
        let chunk: String = repeat(ch).take(n_blocks).collect();
        out += &chunk;
        if is_file {
            file_id += 1
        }
        is_file = !is_file;
    }
    out
}
fn defragment(s: &str) -> String {
    let mut chars: Vec<char> = s.chars().collect();
    loop {
        // move the left pointer to the leftmost empty character
        let left = chars
            .iter()
            .position(|ch| *ch == '.')
            .unwrap();
        // move the right pointer to the rightmost non-empty character
        let right = chars
            .iter()
            .enumerate() // enumerate chars
            .rev() // reverse them
            .find(|(_, ch)| **ch != '.') // find first non-empty one
            .map(|(idx, _)| idx) // return its index
            .unwrap();
        // if the left pointer has moved past the right pointer, it means there
        // are no empty chars on the left anymore, so we can stop
        if left > right {
            break;
        }
        // swap the chars at the left and right positions
        chars.swap(left, right);
    }
    chars.iter().collect()
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), "1928");
    }
    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), "");
    }

    #[test]
    fn test_compute_checksum() {
        let s = "0099811188827773336446555566..............";
        assert_eq!(compute_checksum(s), 1928)
    }

    #[test]
    fn test_expand() {
        let expected = "00...111...2...333.44.5555.6666.777.888899";
        assert_eq!(expand(EXAMPLE), expected);
    }

    #[test]
    fn test_defragment() {
        let expected = "0099811188827773336446555566..............";
        assert_eq!(
            defragment("00...111...2...333.44.5555.6666.777.888899"),
            expected
        );
    }
}
