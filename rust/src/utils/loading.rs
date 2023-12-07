use std::env;
use std::fs;

pub fn load_puzzle_input(filename: &str) -> String {
    let rust_folder = env::current_dir().unwrap();
    let inputs_folder = rust_folder.parent().unwrap().join("_inputs");
    let file_path = inputs_folder.join(filename.to_owned() + ".txt");

    let contents = fs::read_to_string(file_path.as_path())
        .expect("Should have been able to read the file");
    return contents;
}

#[cfg(test)]
mod tests {
    // this makes load_puzzle_input, greet available in the current scope
    // without the absolute path prefix
    use super::*;

    #[test]
    fn test_load_puzzle_input() {
        let result = load_puzzle_input("2023/day1");
        let expected_first_line = "five3onelxjninenine45";
        let first_line = result.lines().next().unwrap();
        println!("{:?}", first_line);
        assert_eq!(first_line, expected_first_line);
    }
}
