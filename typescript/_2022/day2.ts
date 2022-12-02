import {loadPuzzleInput, profile} from "../utils";


const ROCK = 1
const PAPER = 2
const SCISSORS = 3
const LOSE = 1
const DRAW = 2
const WIN = 3
const mapping = {
    A: ROCK,
    B: PAPER,
    C: SCISSORS,
    X: ROCK,
    Y: PAPER,
    Z: SCISSORS,
}

function parseInput(): number[][] {
    let input = loadPuzzleInput("2022/day2")
    return input
        .split("\n")  // ["C Z", "A X", ...]
        .map(
            str => str // "C Z"
                .split(" ")  // ["C", "Z"]
                .map(s => mapping[s])  // [3, 3]
        )
}

function leftWins(left: number, right: number): boolean | null {
    if (left === right) {
        return null  // draw
    }
    return (
        (left === PAPER && right === ROCK)
        || (left === SCISSORS && right === PAPER)
        || (left === ROCK && right === SCISSORS)
    )
}

function scoreRound(opponent: number, you: number): number {
    let points = you
    const outcome = leftWins(you, opponent)
    if (outcome === true) {
        points += 6
    } else if (outcome === false) {
        points += 0
    } else if (outcome === null) {
        points += 3
    } else {
        console.log("JS is busted!")
    }
    return points
}

function selectMove(opponent: number, objective: number): number {
    if (objective === DRAW) {
        return opponent
    } else if (objective === WIN) {
        return {[ROCK]: PAPER, [PAPER]: SCISSORS, [SCISSORS]: ROCK}[opponent]
    } else if (objective === LOSE) {
        return {[ROCK]: SCISSORS, [PAPER]: ROCK, [SCISSORS]: PAPER}[opponent]
    } else {
        console.log("JS is busted!")
    }
}

export function day2Part1(): number {
    const rounds = parseInput()
    let score = 0
    for (let [opponent, you] of rounds) {
        score += scoreRound(opponent, you)
    }
    return score
}

export function day2Part2(): number {
    const rounds = parseInput()
    let score = 0
    for (let [opponent, objective] of rounds) {
        let you = selectMove(opponent, objective)
        score += scoreRound(opponent, you)
    }
    return score
}

if (require.main === module) {
    profile(day2Part1)
    profile(day2Part2)
}