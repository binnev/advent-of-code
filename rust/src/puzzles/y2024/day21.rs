/// Attempt 2:
/// - Figure out the diagonal movements required for each keypad
/// - Propagate those up the robot stack
/// - Delay the choice between horizontal/vertical until the end
///
/// So, desired code: 029A.
/// Numpad looks like this:
/// 7 8 9
/// 4 5 6
/// 1 2 3
///   0 A
///
/// The moves required for the _robot_ operating the numpad are:
/// - move (-1, 0) to 0
/// - enter
/// - move (0, -1) to 2
/// - enter
/// - move (1, -2) to 9
/// - enter
/// - move (0, 3) to A
/// - enter
///
/// To do those moves, we'd need to enter this in the 2nd keypad
/// (arrowpad):
/// - press <
/// - press A
/// - press ^
/// - press A
/// - either press ^^> or >^^
/// - press A
/// - press vvv
/// - press A
///
/// so either:
/// - <A^A^^>AvvvA
/// - <A^A>^^AvvvA
///
/// Arrowpad looks like this:
///   ^ A
/// < v >
///
/// The second robot needs to do these moves:
/// - move (-2, 1) to <
/// - enter
/// - move (1, -1) to ^
/// - enter
/// - move
/// - enter
///
/// To do those moves, we'd need to enter this in the 3rd keypad:
/// - either press <<v or v<<
/// - press A
/// - either press >^ or ^>
/// - press A
///
///
/// I should just brute force it. Only the diagonal moves bifurcate, and
/// there are only 4 layers.
use std::{collections::HashSet, iter::repeat};

use itertools::Itertools;

use crate::utils::{Coord, Direction::*, SparseMatrix};

/// This is not as simple as it looks. If there were just 1 keypad, then all
/// paths would have equal length. However, because there are multiple layers of
/// keypads, and moving the robot's arm from one key to another costs presses,
/// all paths are _not_ equal.
///
/// I suspect that if we make sure all paths are as _straight_ as possible, then
/// they will automatically be the quickest, because it will minimise button
/// switching on the "super" robot.
pub fn part1(input: &str) -> usize {
    let codes: Vec<&str> = input.lines().collect();
    let mut out = 0;
    for code in codes {
        let instructions =
            get_instructions_layered(code, vec![NUMPAD, ARROWPAD, ARROWPAD]);
        let numeric_part: usize = code[..3].parse().unwrap();
        let shortest_instruction_len = instructions
            .iter()
            .map(|s| s.len())
            .min()
            .unwrap();
        let complexity = shortest_instruction_len * numeric_part;
        out += complexity;
    }
    out
}
pub fn part2(input: &str) -> usize {
    0
}
/// Given several keypads, calculate all the inputs that will result in the code
/// being entered on the first keypad
fn get_instructions_layered(code: &str, keypads: Vec<&str>) -> HashSet<String> {
    let mut instructions = HashSet::from([code.to_owned()]);
    for keypad in keypads {
        let mut new_instructions = HashSet::new();
        for code in instructions {
            new_instructions.extend(get_instructions_for_code(&code, keypad));
        }
        instructions = new_instructions;
    }
    instructions
}
/// Get all the ways of entering the given code on the given keypad. Does not
/// include instructions that cross empty squares. Only includes the straightest
/// instructions (i.e. bulk horizontal/vertical)
fn get_instructions_for_code(
    code: &str,   // the code to be entered
    keypad: &str, // the keypad on which we want to enter the code
) -> HashSet<String> {
    let mut instructions: HashSet<String> = HashSet::from(["".into()]);
    let keypad: SparseMatrix<char> = keypad.into();
    let mut cursor = *keypad
        .locate('A')
        .expect(&format!("No 'A' key on keypad {keypad:?}"));
    for letter in code.chars() {
        let to = keypad.locate(letter).unwrap();
        let mut new_instructions = HashSet::new();
        for new_instruction in get_instructions_for_move(&keypad, &cursor, to) {
            for instruction in instructions.iter() {
                new_instructions
                    .insert(instruction.to_owned() + &new_instruction + "A");
            }
        }
        instructions = new_instructions;
        cursor = to.clone();
    }
    instructions
}
/// Try both ways of moving the desired distance -- dx then dy, and vice versa.
/// Return a vec of possible instruction strings
fn get_instructions_for_move(
    keypad: &SparseMatrix<char>,
    from: &Coord,
    to: &Coord,
) -> Vec<String> {
    let mut out = Vec::new();
    let (dx, dy) = (to.clone() - from.clone()).into();

    // horizontal first
    if let Some(instructions) = try_move_horizontal(keypad, from, dx).and_then(
        |(h_instructions, cursor)| {
            try_move_vertical(keypad, &cursor, dy)
                .map(|(v_instructions, _)| h_instructions + &v_instructions)
        },
    ) {
        out.push(instructions);
    }
    // vertical first
    if let Some(instructions) = try_move_vertical(keypad, from, dy).and_then(
        |(v_instructions, cursor)| {
            try_move_horizontal(keypad, &cursor, dx)
                .map(|(h_instructions, _)| v_instructions + &h_instructions)
        },
    ) {
        out.push(instructions);
    }
    out.into_iter().unique().collect()
}
fn try_move_horizontal(
    keypad: &SparseMatrix<char>,
    cursor: &Coord,
    dx: i64,
) -> Option<(String, Coord)> {
    let mut cursor = cursor.clone();
    let direction = if dx > 0 { East } else { West };
    for _ in 0..dx.abs() {
        cursor = cursor.neighbour(direction);
        if is_empty(cursor, &keypad) {
            return None;
        }
    }
    let instructions = repeat(direction.char())
        .take(dx.abs() as usize)
        .collect();
    Some((instructions, cursor))
}
fn try_move_vertical(
    keypad: &SparseMatrix<char>,
    cursor: &Coord,
    dy: i64,
) -> Option<(String, Coord)> {
    let mut cursor = cursor.clone();
    let direction = if dy > 0 { South } else { North };
    for _ in 0..dy.abs() {
        cursor = cursor.neighbour(direction);
        if is_empty(cursor, keypad) {
            return None;
        }
    }
    let instructions = repeat(direction.char())
        .take(dy.abs() as usize)
        .collect();
    Some((instructions, cursor))
}
fn is_empty(key: Coord, keypad: &SparseMatrix<char>) -> bool {
    keypad.get(&key) == Some(&' ')
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 126384);
    }
    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 0);
    }
    #[test]
    fn test_get_instructions_for_move() {
        let keypad: SparseMatrix<char> = NUMPAD.into();
        let from = keypad.locate('A').unwrap();

        // If there's no empty square in the way, we should get both ways
        let to = keypad.locate('2').unwrap();
        let instructions = get_instructions_for_move(&keypad, from, to);
        assert_eq!(instructions, ["<^", "^<"]);

        // if there's an empty square in the way, we should only get 1 option
        let to = keypad.locate('1').unwrap();
        let instructions = get_instructions_for_move(&keypad, from, to);
        assert_eq!(instructions, ["^<<"]);

        // horizontal only
        let to = keypad.locate('0').unwrap();
        let instructions = get_instructions_for_move(&keypad, from, to);
        assert_eq!(instructions, ["<"]);

        // vertical only
        let to = keypad.locate('6').unwrap();
        let instructions = get_instructions_for_move(&keypad, from, to);
        assert_eq!(instructions, ["^^"]);

        // no movement
        let to = from.clone();
        let instructions = get_instructions_for_move(&keypad, from, &to);
        assert_eq!(instructions, [""]);
    }

    #[test]
    fn test_get_instructions_for_code() {
        let instructions = get_instructions_for_code("029A", NUMPAD);
        // The three shortest instructions are
        // <A^A>^^AvvvA
        // <A^A^^>AvvvA
        // <A^A^>^AvvvA
        // but it won't bother reporting the last one, because it alternates ^>^
        // which is inefficient.
        assert_eq!(
            instructions,
            ["<A^A>^^AvvvA", "<A^A^^>AvvvA"]
                .into_iter()
                .map(|s| s.to_owned())
                .collect()
        );
        // POTENTIAL GOTCHA: the human _may_ enter the last one without losing
        // efficiency, so this approach may cause us to overlook a solution
    }

    #[test]
    fn test_get_instructions_layered() {
        let instructions = get_instructions_layered("029A", vec![NUMPAD]);
        let shortest = instructions
            .iter()
            .map(|i| i.len())
            .min()
            .unwrap();
        assert_eq!(shortest, "<A^A>^^AvvvA".len());

        let instructions =
            get_instructions_layered("029A", vec![NUMPAD, ARROWPAD]);
        let shortest = instructions
            .iter()
            .map(|i| i.len())
            .min()
            .unwrap();
        assert_eq!(shortest, "v<<A>>^A<A>AvA<^AA>A<vAAA>^A".len());

        let instructions =
            get_instructions_layered("029A", vec![NUMPAD, ARROWPAD, ARROWPAD]);
        let shortest = instructions
            .iter()
            .map(|i| i.len())
            .min()
            .unwrap();
        assert_eq!(shortest, "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A".len());

        for (code, shortest_instructions) in [
            ("029A", "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A"),
            ("179A", "<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"),
            ("379A", "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"),
            ("456A", "<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A"),
            ("980A", "<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A"),
        ] {
            let instructions = get_instructions_layered(code, vec![NUMPAD, ARROWPAD, ARROWPAD]);
            let shortest = instructions
            .iter()
            .map(|i| i.len())
            .min()
            .unwrap();
            assert_eq!(
                shortest,
                shortest_instructions.len(),
                "Fail: {code}",
            )
        }
    }
}
pub const EXAMPLE: &str = "029A
980A
179A
456A
379A";
pub const NUMPAD: &str = "789
456
123
 0A";
pub const ARROWPAD: &str = " ^A
<v>";
