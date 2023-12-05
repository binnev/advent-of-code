pub fn part1() -> &'static str {
    let s = "hi";
    return s;
}

pub fn part2() -> &'static str {
    return "";
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let result = part1();
        assert_eq!(result, "hi");
    }

    #[test]
    fn test_part2() {
        let result = part2();
        assert_eq!(result, "");
    }
}
