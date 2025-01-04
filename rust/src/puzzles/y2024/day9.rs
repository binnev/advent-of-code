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
    let mut block_start = 0;
    for block in disk {
        if let Some(number) = block.file_id {
            for ii in block_start..block_start + block.size {
                out += number * ii;
            }
        }
        block_start += block.size;
    }
    out
}
/// Expand input "12345" into "0..111....22222" but instead of using a string
/// (which is limited to max value 9 per position) we use a vec. Each item in
/// the vec describes a block, which can either be a file, or empty. So "22222"
/// would be Block{file_id: 2, size:5}
fn expand(s: &str) -> Disk {
    let mut is_file = true;
    let mut out = vec![];
    let mut file_id = 0;
    for ch in s.chars() {
        let block_size = ch
            .to_digit(10)
            .expect(&format!("Couldn't parse {ch} to digit!"))
            as usize; // input is only numbers
        let block = Block {
            file_id: if is_file { Some(file_id) } else { None },
            size:    block_size,
        };
        out.push(block);
        if is_file {
            file_id += 1
        }
        is_file = !is_file;
    }
    out
}
// Squash the contents of the disk to the left, creating more contiguous free
// space, but fragmenting the files in the process. Assume that we created one
// file block per character in the input
fn fragment(disk: &mut Disk) {
    loop {
        // move the left pointer to the leftmost empty character
        let empty_pos = disk
            .iter()
            .position(|block| block.file_id.is_none())
            .unwrap();
        // move the right pointer to the rightmost non-empty character
        let file_pos = disk
            .iter()
            .enumerate() // enumerate chars
            .rev() // reverse them
            .find(|(_, block)| block.file_id.is_some()) // find first non-empty one
            .map(|(idx, _)| idx) // return its index
            .unwrap();
        // if the left pointer has moved past the right pointer, it means there
        // are no empty chars on the left anymore, so we can stop
        if empty_pos > file_pos {
            break;
        }
        // move the right block "one by one" into the left block.
        let empty = &disk[empty_pos];
        let file = &disk[file_pos];

        if empty.size == file.size {
            // Same size: simply swap the file with the empty space
            disk.swap(empty_pos, file_pos);
        } else if empty.size > file.size {
            // Empty space > file:
            // divide the empty block into 2; 1 the size of the file, and 1
            // empty remainder
            // 1. Set empty space to be size of file
            // 2. Swap empty space and file
            // 3. Insert empty remainder after the file
            let remainder = empty.size - file.size;
            disk[empty_pos].size = file.size;
            disk.swap(empty_pos, file_pos);
            disk.insert(
                empty_pos + 1,
                Block {
                    file_id: None,
                    size:    remainder,
                },
            );
        } else {
            // File > empty space:
            // Divide the file into 2; 1 the size of the empty space, and 1
            // file remainder.
            // 1. Set file to be size of empty space
            // 2. Swap empty space and file
            // 3. Insert file remainder after the empty space
            let remainder = file.size - empty.size;
            let file_id = file.file_id;
            disk[file_pos].size = empty.size;
            disk.swap(empty_pos, file_pos);
            disk.insert(
                file_pos + 1,
                Block {
                    file_id,
                    size: remainder,
                },
            );
        }
    }
}
type FileId = usize;
type Disk = Vec<Block>;
struct Block {
    file_id: Option<FileId>,
    size:    usize,
}

#[cfg(test)]
mod tests {
    use super::*;
    use itertools::Itertools;

    fn stringify_disk(disk: &Disk) -> String {
        let mut out: Vec<String> = vec![];
        for block in disk {
            for _ in 0..block.size {
                let ch = match block.file_id {
                    Some(fid) => fid.to_string(),
                    None => ".".into(),
                };
                out.push(ch);
            }
        }
        out.join("")
    }
    /// from an expanded string, that is, so something like:
    /// 00...111...2...333.44.5555.6666.777.888899
    fn disk_from_string(s: &str) -> Disk {
        let mut out = vec![];
        let chunks: Vec<String> = s
            .chars()
            .chunk_by(|&c| c)
            .into_iter()
            .map(|(_, group)| group.collect())
            .collect();
        for chunk in chunks {
            let ch = chunk.chars().next().unwrap();
            let file_id = match ch {
                '.' => None,
                _ => Some(ch.to_digit(10).unwrap() as usize),
            };
            out.push(Block {
                file_id: file_id,
                size:    chunk.len(),
            })
        }
        out
    }
    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), "1928");
    }
    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), "2858");
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
    fn test_fragment() {
        let mut disk = expand(EXAMPLE);
        fragment(&mut disk);
        let expected = "0099811188827773336446555566..............";
        let stringified = stringify_disk(&disk);
        assert_eq!(stringified, expected);
    }
}
