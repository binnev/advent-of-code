use regex::Regex;

// Just listen to the mul instructions
pub fn part1(input: &str) -> usize {
    let commands = parse(input);
    let mut out = 0;
    for cmd in commands {
        match cmd {
            Command::Mul(left, right) => out += left * right,
            _ => {}
        }
    }
    out
}

pub fn part2(input: &str) -> usize {
    let commands = parse(input);
    let mut enabled = true;
    let mut out = 0;
    for cmd in commands {
        match cmd {
            Command::Do => enabled = true,
            Command::Dont => enabled = false,
            Command::Mul(left, right) => {
                if enabled {
                    out += left * right
                }
            }
        }
    }
    out
}

fn parse(input: &str) -> Vec<Command> {
    let rx = Regex::new(
        [
            r"(?P<cmd>do|don't|mul)",               // instruction
            r"\((?P<left>\d+)?,?(?P<right>\d+)?\)", // optional args for mul
        ]
        .join("")
        .as_str(),
    )
    .unwrap();
    let mut out = vec![];
    for cap in rx.captures_iter(input) {
        match cap
            .name("cmd")
            .expect(&format!("expected cap to have 1 arg: {:?}", cap.get(0)))
            .as_str()
        {
            "mul" => {
                let left = cap
                    .name("left")
                    .expect("mul command without args!")
                    .as_str()
                    .parse()
                    .unwrap();
                let right = cap
                    .name("right")
                    .expect("mul command without args!")
                    .as_str()
                    .parse()
                    .unwrap();
                out.push(Command::Mul(left, right));
            }
            "do" => out.push(Command::Do),
            "don't" => out.push(Command::Dont),
            _ => panic!("Unrecognized match! {cap:?}"),
        }
    }
    out
}
const EXAMPLE: &str =
    "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))";

const EXAMPLE2: &str =
    "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))";

#[derive(PartialEq, Debug)]
enum Command {
    Mul(usize, usize),
    Do,
    Dont,
}
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 161);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE2), 48);
    }

    #[test]
    fn test_parse() {
        assert_eq!(
            parse(EXAMPLE),
            vec![
                Command::Mul(2, 4),
                Command::Mul(5, 5),
                Command::Mul(11, 8),
                Command::Mul(8, 5)
            ]
        );
        assert_eq!(
            parse(EXAMPLE2),
            vec![
                Command::Mul(2, 4),
                Command::Dont,
                Command::Mul(5, 5),
                Command::Mul(11, 8),
                Command::Do,
                Command::Mul(8, 5)
            ]
        )
    }
}
