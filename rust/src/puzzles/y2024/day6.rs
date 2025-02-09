use std::collections::HashSet;

use crate::utils::{Coord, Direction, Direction::*, SparseMatrix};

const OBSTACLE: char = '#';

// Find the number of unique squares visited by the guard
pub fn part1(input: &str) -> usize {
    let mut map = parse(input);
    let guard = remove_guard(&mut map);
    let (history, _) = trace_guard(&map, vec![guard]);
    let unique_positions: HashSet<Coord> = history
        .iter()
        .map(|guard| guard.position)
        .collect();
    unique_positions.len()
}

/// Part 2 take 2
///
/// Guard's path:
///....#.....
/// ....XXXXX#
/// ....X...X.
/// ..#.X...X.
/// ..XXXXX#X.
/// ..X.X.X.X.
/// .#XXXXXXX.
/// .XXXXXXX#.
/// #XXXXXXX..
/// ......#X..
///
/// ...<#.....
/// ...v+---+#
/// ...v|...|.
/// ..#v|...|.
/// ...v|..#|.
/// ...v|...|.
/// .#.O^---+.
/// ........#.
/// #.........
/// ......#...
///
/// ....#.....
/// ....+---+#
/// ....|...|.
/// ..#.|...|.
/// ..+-+-+#|.
/// ..|.|.|.|.
/// .#+-^-+-+.
/// .v>>>>O.#.
/// #.........
/// ......#...
///
/// ....#.....
/// ....+---+#
/// ....|...|.
/// ..#.|...|.
/// ..+-+-+#|.
/// ..|.|.|.|.
/// .#+-^-+-+.
/// .+----+O#.
/// #+----+^..
/// ......#>..
///
/// For every existing obstacle,
/// take 1 step WEST and look SOUTH. Get every intersection with the path
/// travelling WEST
///
/// take 1 step NORTH and look WEST. Get every intersection with the path
/// travelling NORTH
///
/// take 1 step EAST and look NORTH. Get every intersection with the path
/// travelling EAST
///
/// take 1 step X and look X-1. Get every intersection with the path travelling
/// X.
///
/// stop searching when you hit the first obstacle.
///
/// Once we've found this much smaller set of valid obstacle points, we check
/// all those for infinite loops.
///
/// TAKE 3:
/// Reducing the search space like this ^ didn't help much. The guard's path is
/// 5554 long, found 4788 potential obstacles. So most of the guard's path is
/// potential obstacles. We need to speed up the checking for infinite loops.
///
/// Currently we insert the new obstacle and trace the guard from the beginning.
/// Which is around 5000 steps. What we could do is keep the original guard path
/// up to where it collides with the new obstacle, and then simulate from then
/// on.
///
/// - Keep an ordered guard path -- Vec<Guard> instead of HashSet<Guard>
/// - Make a function that can accept a partial path and continue iterating it
///   -- maybe iter_guard can continue doing this?

// Insert an obstacle into every square, and check if that produces an infinite
// loop for the guard. Count the infinite loops.
pub fn part2(input: &str) -> usize {
    let mut map = parse(input);
    let start = remove_guard(&mut map);
    let (history, _) = trace_guard(&map, vec![start.clone()]);
    let mut infinite_loops = 0;

    let unique_positions: HashSet<Coord> = history
        .iter()
        .map(|g| g.position)
        .collect();
    // For now just try inserting an obstacle into every square visited by the
    // guard.
    for obstacle_position in unique_positions {
        // not allowed to insert an obstacle at the starting point
        if obstacle_position == start.position {
            continue;
        }
        // For every square, try inserting an obstacle, and check if there's an
        // infinite loop.
        map.insert(obstacle_position, OBSTACLE);
        // Reuse the guard's path up to where it intersects the new obstacle.
        // Then simulate from then on.
        let last_step_before_collision = history
            .iter()
            .enumerate()
            .find(|(_, guard)| guard.position == obstacle_position)
            .map(|x| x.0)
            .expect("Obstacle doesn't intersect guard path?!");
        let new_history = history[..last_step_before_collision].to_vec();

        let (_, result) = trace_guard(&map, new_history);
        match result {
            TraceResult::InfiniteLoop => infinite_loops += 1,
            _ => {} // do nothing for out of bounds
        }
        map.insert(obstacle_position, '.'); // remove obstacle
    }

    infinite_loops
}

// Iterate the guard until it either goes out of bounds or enters an infinite
// loop
fn trace_guard(
    map: &SparseMatrix<char>,
    history: Vec<Guard>,
) -> (Vec<Guard>, TraceResult) {
    let mut history = history;
    // use a set for fast lookup
    let mut unique: HashSet<Guard> = history.clone().into_iter().collect();
    // Continue iterating from the end of the history.
    let mut guard = history
        .iter()
        .last()
        .expect("Got empty history!")
        .clone();
    loop {
        iter_guard(&map, &mut guard);
        // if the guard's position is not in the map, it has gone out of bounds
        if !map.contains_key(&guard.position) {
            return (history, TraceResult::OutOfBounds);
        }
        // if the guard assumes a position that we've seen before, it means
        // we've entered an infinite loop
        if unique.contains(&guard) {
            return (history, TraceResult::InfiniteLoop);
        }
        history.push(guard.clone());
        unique.insert(guard.clone());
    }
}
enum TraceResult {
    OutOfBounds,
    InfiniteLoop,
}

pub const EXAMPLE: &str = "....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...";

#[derive(Hash, PartialEq, Eq, Clone)]
struct Guard {
    direction: Direction,
    position:  Coord,
}
impl Guard {
    fn next_square(&self) -> Coord {
        let Coord(x, y) = self.position; // yay, destructuring sugar
        match self.direction {
            North => Coord(x, y - 1), // y is positive down
            East => Coord(x + 1, y),
            South => Coord(x, y + 1),
            West => Coord(x - 1, y),
        }
    }
    fn turn_right(&mut self) {
        self.direction = self.direction.clockwise();
    }
    fn walk(&mut self) {
        self.position = self.next_square();
    }
}

/// Move the guard, turning if necessary. Bear in mind that we may need to turn
/// multiple times.
fn iter_guard(map: &SparseMatrix<char>, guard: &mut Guard) {
    while map.get(&guard.next_square()) == Some(&OBSTACLE) {
        guard.turn_right();
    }
    guard.walk();
}

/// Remove the guard from the map, and return its position. Assuming the guard
/// always starts facing north
fn remove_guard(map: &mut SparseMatrix<char>) -> Guard {
    for (coord, ch) in map.iter_mut() {
        if *ch == '^' {
            *ch = '.'; // set to empty
            return Guard {
                position:  coord.clone(),
                direction: North,
            };
        }
    }
    unreachable!() // if no guard in map
}

fn parse(input: &str) -> SparseMatrix<char> {
    let mut map = SparseMatrix::new();
    for (y, row) in input.lines().enumerate() {
        for (x, ch) in row.chars().enumerate() {
            let coord = Coord(x as i64, y as i64);
            map.insert(coord, ch);
        }
    }
    map
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 41);
    }
    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 6);
    }
}
