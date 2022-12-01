import {loadPuzzleInput, profile} from "../utils";

function parseInput(): number[] {
    const input = loadPuzzleInput("2020/day1")
    return input.split("\n").map(s => parseInt(s, 10))
}

export function day1Part1(): number {
    const integers = parseInput()
    for (let a of integers) {
        for (let b of integers) {
            if (a + b === 2020) {
                return a * b
            }
        }
    }
}

export function day1Part2(): number {
    const integers = parseInput()
    for (let a of integers) {
        for (let b of integers) {
            for (let c of integers) {
                if (a + b + c === 2020) {
                    return a * b * c
                }
            }
        }
    }
}

if (require.main === module) {
    profile(day1Part1)
    profile(day1Part2)
}