#[cfg(test)]
mod tests {
    use crate::puzzles::y2023::day1::*;
    use crate::utils;

    #[test]
    fn test_load_puzzle_input() {
        let input = utils::load_puzzle_input("2023/day1");
        let result = part1(&input);
        let expected = "55123";
        assert_eq!(result, expected);
    }
}
