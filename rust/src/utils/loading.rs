pub fn load_puzzle_input(filename: &str) -> &'static str {
    println!("loader received {filename}");
    return "xoxoox"; // todo: implement
}

pub fn greet(name: &str) {
    println!("Hello, {name}!");
}

#[cfg(test)]
mod tests {
    // this makes load_puzzle_input, greet available in the current scope
    // without the absolute path prefix
    use super::*;

    #[test]
    fn test_load_puzzle_input() {
        let result = load_puzzle_input("hello");
        assert_eq!(result, "");
    }
}
