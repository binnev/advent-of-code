use regex::Regex;

pub fn part1(input: &str) -> String {
    let limit = Hand {
        r: 12,
        g: 13,
        b: 14,
    };
    let games: Vec<(u32, Vec<Hand>)> = input
        .lines()
        .map(parse_game)
        .collect::<Result<_, _>>()
        .unwrap();
    let mut result = 0;
    for (ii, game) in games {
        if is_game_possible(game, &limit) {
            result += ii;
        }
    }
    format!("{result}")
}
pub fn part2(input: &str) -> String {
    todo!()
}
const EXAMPLE: &str = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green";

fn is_game_possible(game: Vec<Hand>, limit: &Hand) -> bool {
    for hand in game {
        if hand.r > limit.r || hand.b > limit.b || hand.g > limit.g {
            return false;
        }
    }
    true
}
fn parse_game(game: &str) -> Result<(u32, Vec<Hand>), String> {
    let game_rx =
        Regex::new(r#"Game (\d+): (.*)"#).map_err(|err| format!("{err:?}"))?;
    let caps = game_rx
        .captures(game)
        .ok_or(format!("Couldn't parse game: {game}"))?;
    let game_id: u32 = caps[1].parse().map_err(|err| format!("{err:?}"))?;
    let rest = &caps[2];
    let hands = rest.split("; ").map(parse_hand).collect::<Result<_, _>>()?;
    Ok((game_id, hands))
}

fn parse_hand(hand_str: &str) -> Result<Hand, String> {
    let mut hand = Hand::default();
    for cubes in hand_str.split(", ") {
        let (amount, colour) = parse_cubes(cubes)?;
        match colour {
            "red" => hand.r = amount,
            "green" => hand.g = amount,
            "blue" => hand.b = amount,
            _ => return Err(format!("Unknown colour {colour}!")),
        };
    }
    Ok(hand)
}

fn parse_cubes(cubes: &str) -> Result<(u32, &str), String> {
    let colour_rx = Regex::new(r#"(\d+) (red|green|blue)"#).unwrap();
    let caps = match colour_rx.captures(cubes) {
        Some(caps) => Ok(caps),
        None => Err(format!("Couldn't parse cubes: {cubes}")),
    }?;
    let amount: u32 = match caps[1].parse() {
        Ok(amount) => Ok(amount),
        Err(_) => Err(format!("Couldn't parse cube number {cubes}")),
    }?;
    let colour = match caps.get(2) {
        Some(c) => Ok(c.as_str()),
        None => Err("Indexerror getting colour!"),
    }?;
    Ok((amount, colour))
}

// fn parse_input(input: &str) -> Vec<(u32, Vec<Hand>)> {
//     let output = vec![];
//     for line in input.lines() {
//         let hands: Vec<Hand> = vec![];
//         match line_rx.captures(line) {
//             Some(caps) => {
//                 let game_id: u32 = caps[1].parse().unwrap();
//                 let rest = &caps[2];
//                 println!("{game_id}: {rest}");
//                 for hand_string in rest.split("; ") {
//                     println!("hand_string={hand_string}");
//                     for ccc in colour_rx.captures(hand_string).iter() {
//                         println!("{:?}", ccc);
//                     }
//                 }
//             }
//             None => panic!("Couldn't parse line: {line}"),
//         }
//     }
//     output
// }

#[derive(Default, Debug)]
struct Hand {
    r: u32,
    g: u32,
    b: u32,
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), "8")
    }

    #[test]
    fn test_parse_game() {
        assert_eq!(parse_cubes(""), Err("Couldn't parse cubes: ".into()));
        assert_eq!(parse_cubes("3 red"), Ok((3, "red")));
        assert_eq!(
            parse_cubes("99999999999999 red"),
            Err("Couldn't parse cube number 99999999999999 red".into())
        );
        assert_eq!(
            parse_cubes("four red"),
            Err("Couldn't parse cubes: four red".into())
        );
    }
}
