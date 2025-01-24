use std::{
    collections::{HashMap, HashSet},
    iter, thread,
    time::Duration,
};

use crate::utils::{Coord, Direction, SparseMatrix};

pub fn part1(input: &str) -> usize {
    let maze: SparseMatrix<char> = input.into();
    let start = Reindeer {
        position:  maze
            .iter()
            .find_map(
                |(coord, ch)| if ch == &START { Some(coord) } else { None },
            )
            .expect("No 'S' square in maze!")
            .clone(),
        direction: Direction::East,
    };
    let end = maze
        .iter()
        .find_map(|(coord, ch)| if ch == &END { Some(coord) } else { None })
        .expect("No 'E' square in maze!");
    dijkstra(&start, end, &maze).expect("No path from S to E!")
}
pub fn part2(input: &str) -> usize {
    let map: SparseMatrix<char> = input.into();
    let start = Reindeer {
        position:  map
            .iter()
            .find_map(
                |(coord, ch)| if ch == &START { Some(coord) } else { None },
            )
            .expect("No 'S' square in maze!")
            .clone(),
        direction: Direction::East,
    };
    let end = map
        .iter()
        .find_map(|(coord, ch)| if ch == &END { Some(coord) } else { None })
        .expect("No 'E' square in maze!");
    let best_paths =
        find_all_best_paths(&start, end, &map).expect("No best paths found!");
    let mut tiles: HashSet<Coord> = HashSet::new();
    for path in best_paths {
        tiles.extend(
            path.path
                .into_iter()
                .map(|reindeer| reindeer.position),
        );
    }
    tiles.len()
}
/// Keep track of each Reindeer's path so that we can find all the squares that
/// belong to one of the best paths.
fn find_all_best_paths(
    start: &Reindeer,
    end: &Coord,
    map: &SparseMatrix<char>,
) -> Option<Vec<ReindeerPath>> {
    // We use this to remember the best store for any given Reindeer. This is
    // used to kill bad paths early.
    let mut best_scores: HashMap<Reindeer, usize> =
        HashMap::from([(start.clone(), 0)]);
    let mut finished_paths: Vec<ReindeerPath> = vec![];
    let mut paths: HashSet<ReindeerPath> = HashSet::from([ReindeerPath {
        path:  vec![start.clone()],
        score: 0,
    }]);
    loop {
        let mut new_paths = HashSet::new();
        for path in paths.iter() {
            let reindeer = path
                .path
                .last()
                .expect("Empty ReindeerPath!");
            // Explore every possible neighbouring square
            for (movement_cost, new_reindeer) in get_neighbours(reindeer, map) {
                let new_score = path.score + movement_cost;
                match best_scores.get(&new_reindeer) {
                    // If the best score is better, discard this path,
                    // because we know it is suboptimal
                    Some(&best_score) if best_score < new_score => {}
                    // If the new score is equal to or better than the best
                    // score (or if there is no best score) then continue
                    // exploring this path
                    _ => {
                        best_scores.insert(new_reindeer, new_score);
                        let mut new_path = path.clone();
                        new_path.path.push(new_reindeer);
                        new_path.score = new_score;
                        if map.get(&new_reindeer.position) == Some(&END) {
                            finished_paths.push(new_path);
                        } else {
                            new_paths.insert(new_path);
                        }
                    }
                }
            }
        }
        if new_paths.len() == 0 {
            break;
        }
        paths = new_paths;
    }
    // There may be multiple reindeer that arrived at the end square in
    // different orientations. We are interested in the minimum score.
    let best_score = best_scores
        .into_iter()
        .filter(|(reindeer, _)| reindeer.position == *end)
        .min_by_key(|(_, score)| *score)
        .map(|(_, score)| score)?;

    // Return all the paths that have the best score
    Some(
        finished_paths
            .into_iter()
            .filter(|path| path.score == best_score)
            .collect(),
    )
}
#[derive(PartialEq, Eq, Hash, Debug, Clone)]
struct ReindeerPath {
    path:  Vec<Reindeer>,
    score: usize,
}
/// Use Dijkstra's algorithm to find the shortest path (by steps and turn
/// weighting) from S to E. The reindeer always starts facing East.
///
/// Let's make the scores decoupled from the reindeer's direction -- i.e. a
/// _position_ has a score, and that's it.
///
/// If there is no path from S to E, return None.
fn dijkstra(
    start: &Reindeer,
    end: &Coord,
    map: &SparseMatrix<char>,
) -> Option<usize> {
    let mut scores: HashMap<Reindeer, usize> =
        HashMap::from([(start.clone(), 0)]);
    let mut frontier: HashSet<Reindeer> = HashSet::from([start.clone()]);
    loop {
        let mut new_frontier = HashSet::new();
        for reindeer in frontier.iter() {
            let current_score = scores.get(&reindeer).unwrap().clone();
            for (movement_cost, new_reindeer) in get_neighbours(reindeer, map) {
                // Always calculate the score, regardless of whether the new
                // position has been reached yet. This allows us to improve the
                // score of previously recorded positions.
                let new_score = current_score + movement_cost;
                // if the new score is lower than the existing score, update the
                // existing score, and also add this reindeer to the new
                // frontier to continue exploring. This means that we don't
                // continue exploring reindeer with worse scores.
                match scores.get(&new_reindeer) {
                    Some(&old_score) if old_score < new_score => {
                        // If the old score is better, discard the reindeer
                    }
                    _ => {
                        scores.insert(new_reindeer, new_score);
                        if map.get(&new_reindeer.position) != Some(&END) {
                            new_frontier.insert(new_reindeer);
                        }
                    }
                }
            }
        }
        if new_frontier.len() == 0 {
            break;
        }
        frontier = new_frontier;
    }
    // There may be multiple reindeer that arrived at the end square in
    // different orientations. We are interested in the minimum score.
    scores
        .into_iter()
        .filter(|(reindeer, _)| reindeer.position == *end)
        .min_by_key(|(_, score)| *score)
        .map(|(_, score)| score)
}
fn print_stuff(
    map: &SparseMatrix<char>,
    frontier: &HashSet<Reindeer>,
    scores: &HashMap<Reindeer, usize>,
) {
    let mut printable: SparseMatrix<String> = SparseMatrix {
        contents: map
            .contents
            .iter()
            .map(|(coord, ch)| (coord.clone(), format!("{ch}")))
            .collect(),
    };
    for (reindeer, score) in scores {
        match map.get(&reindeer.position) {
            Some(&START) | Some(&END) => continue,
            _ => {
                let turns = score / TURN_COST;
                printable.insert(reindeer.position.clone(), format!("{turns}"));
            }
        }
    }
    for reindeer in frontier {
        printable.insert(
            reindeer.position,
            format!("{}", reindeer.direction.arrow()),
        );
    }
    println!("{printable}");
}
/// Get the neighbouring positions available to the given reindeer, along with
/// their costs. The results should always be new squares (i.e. not turning
/// 90deg and staying on the same square)
fn get_neighbours(
    reindeer: &Reindeer,
    map: &SparseMatrix<char>,
) -> Vec<(usize, Reindeer)> {
    let mut out = vec![];
    // Try moving forward/left/right, if there's an empty square there. Don't
    // include the square directly behind the reindeer, because we assume it
    // just came from there and we're not interested in backtracking.
    for (cost, new_direction) in [
        (STEP_COST, reindeer.direction),
        (
            TURN_COST + STEP_COST,
            reindeer.direction.counter_clockwise(),
        ),
        (TURN_COST + STEP_COST, reindeer.direction.clockwise()),
    ] {
        let new_position = reindeer
            .position
            .neighbour(new_direction);
        match map.get(&new_position) {
            Some(&WALL) | None => {}
            _ => out.push((
                cost,
                Reindeer {
                    position:  new_position,
                    direction: new_direction,
                },
            )),
        }
    }
    out
}
#[derive(PartialEq, Eq, Hash, Debug, Clone, Copy)]
struct Reindeer {
    position:  Coord,
    direction: Direction,
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 7036);
        assert_eq!(part1(EXAMPLE2), 11048);
    }
    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 45);
        assert_eq!(part2(EXAMPLE2), 64);
    }
}
const EXAMPLE: &str = "###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############";
const EXAMPLE2: &str = "#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################";
const EMPTY: char = '.';
const WALL: char = '#';
const START: char = 'S';
const END: char = 'E';
const TURN_COST: usize = 1000;
const STEP_COST: usize = 1;
