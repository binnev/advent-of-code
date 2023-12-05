pub fn load_puzzle_input(filename: &str) -> &str {
    return "";
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_load_puzzle_input() {
        let result = load_puzzle_input("hello");
        assert_eq!(result, "");
    }
}
