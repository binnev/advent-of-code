pub fn part1(input: &str) -> usize {
    let mut stones = parse(input);
    for _ in 0..25 {
        stones = evolve_stones(stones);
    }
    stones.len()
}
pub fn part2(input: &str) -> usize {
    0
}
/// If the stone is engraved with the number 0, it is replaced by a stone
/// engraved with the number 1.
///
/// If the stone is engraved with a number that has an even number of digits,
/// it is replaced by two stones. The left half of the digits are engraved on
/// the new left stone, and the right half of the digits are engraved on the new
/// right stone. (The new numbers don't keep extra leading zeroes: 1000 would
/// become stones 10 and 0.)
///
/// If none of the other rules apply, the stone is replaced by a new stone; the
/// old stone's number multiplied by 2024 is engraved on the new stone.
fn evolve_stones(stones: Vec<usize>) -> Vec<usize> {
    let mut out = vec![];
    for stone in stones {
        let stringified = format!("{stone}");
        let len = stringified.len();
        if stone == 0 {
            out.push(1)
        } else if len % 2 == 0 {
            let middle = len / 2;
            let left: usize = stringified[..middle].parse().unwrap();
            let right: usize = stringified[middle..].parse().unwrap();
            out.push(left);
            out.push(right);
        } else {
            out.push(stone * 2024)
        }
    }
    out
}
const EXAMPLE: &str = "125 17";
fn parse(input: &str) -> Vec<usize> {
    input
        .split_whitespace()
        .map(|s| {
            s.parse()
                .expect(&format!("Couldn't parse number: {s}"))
        })
        .collect()
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 55312);
    }
    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 0);
    }

    #[test]
    fn test_evolve_stones() {
        let stones: Vec<usize> = vec![125, 17];
        let stones = evolve_stones(stones);
        assert_eq!(stones, vec![253000, 1, 7]);
        let stones = evolve_stones(stones);
        assert_eq!(stones, vec![253, 0, 2024, 14168]);
        let stones = evolve_stones(stones);
        assert_eq!(stones, vec![512072, 1, 20, 24, 28676032]);
        let stones = evolve_stones(stones);
        assert_eq!(stones, vec![512, 72, 2024, 2, 0, 2, 4, 2867, 6032]);
        let stones = evolve_stones(stones);
        assert_eq!(
            stones,
            vec![1036288, 7, 2, 20, 24, 4048, 1, 4048, 8096, 28, 67, 60, 32]
        );
        let stones = evolve_stones(stones);
        assert_eq!(
            stones,
            vec![
                2097446912, 14168, 4048, 2, 0, 2, 4, 40, 48, 2024, 40, 48, 80,
                96, 2, 8, 6, 7, 6, 0, 3, 2
            ]
        );
    }
}
