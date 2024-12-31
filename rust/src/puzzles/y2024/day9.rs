pub fn part1(input: &str) -> String {
    let mut disk = expand(input.trim());
    fragment(&mut disk);
    let checksum = compute_checksum(&disk);
    format!("{checksum}")
}
pub fn part2(input: &str) -> String {
    "".into()
}
const EXAMPLE: &str = "2333133121414131402";
fn compute_checksum(disk: &Disk) -> usize {
    let mut out = 0;
    for (ii, block) in disk.iter().enumerate() {
        match block {
            Some(file_id) => out += file_id * ii,
            None => break, // Assume everything to the right is also empty
        }
    }
    out
}
/// Expand input "12345" into "0..111....22222" but instead of using a string
/// (which is limited to max value 9 per position) we use a vec. Each position
/// in the vec can contain either a file id, or None.
fn expand(s: &str) -> Disk {
    let mut is_file = true;
    let mut out = vec![];
    let mut file_id = 0;
    for n_blocks in s.chars() {
        let n_blocks = n_blocks
            .to_digit(10)
            .expect(&format!("Couldn't parse {n_blocks} to digit!"))
            as usize; // input is only numbers
        let block = match is_file {
            true => Some(file_id),
            false => None,
        };
        for _ in 0..n_blocks {
            out.push(block.clone());
        }
        if is_file {
            file_id += 1
        }
        is_file = !is_file;
    }
    out
}
// Squash the contents of the disk to the left, creating more contiguous free
// space, but fragmenting the files in the process.
fn fragment(disk: &mut Disk) {
    loop {
        // move the left pointer to the leftmost empty character
        let left = disk
            .iter()
            .position(|block| block.is_none())
            .unwrap();
        // move the right pointer to the rightmost non-empty character
        let right = disk
            .iter()
            .enumerate() // enumerate chars
            .rev() // reverse them
            .find(|(_, block)| block.is_some()) // find first non-empty one
            .map(|(idx, _)| idx) // return its index
            .unwrap();
        // if the left pointer has moved past the right pointer, it means there
        // are no empty chars on the left anymore, so we can stop
        if left > right {
            break;
        }
        // swap the chars at the left and right positions
        disk.swap(left, right);
    }
}
type FileId = usize;
type Disk = Vec<Option<FileId>>;

#[cfg(test)]
mod tests {
    use super::*;

    fn stringify_disk(disk: &Disk) -> String {
        disk.iter()
            .map(|block| match block {
                Some(file_id) => file_id.to_string(),
                None => ".".into(),
            })
            .collect()
    }
    fn disk_from_string(s: &str) -> Disk {
        s.chars()
            .map(|ch| match ch {
                '.' => None,
                _ => Some(ch.to_digit(10).unwrap() as usize),
            })
            .collect()
    }
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
        let disk = disk_from_string(s);
        assert_eq!(compute_checksum(&disk), 1928)
    }

    #[test]
    fn test_expand() {
        let expected = "00...111...2...333.44.5555.6666.777.888899";
        let disk = expand(EXAMPLE);
        let stringified = stringify_disk(&disk);
        assert_eq!(stringified, expected);
    }

    #[test]
    fn test_defragment() {
        let mut disk = expand(EXAMPLE);
        fragment(&mut disk);
        let expected = "0099811188827773336446555566..............";
        let stringified = stringify_disk(&disk);
        assert_eq!(stringified, expected);
    }
}
