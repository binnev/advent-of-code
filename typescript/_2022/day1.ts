import {loadPuzzleInput, profile} from "../utils";

function getCalories(): number[] {
    const input = loadPuzzleInput("2022/day1")
    return input
        .split("\n\n")
        .map(elf => elf
            .split("\n")
            .map(s => parseInt(s, 10))
            .reduce((a, b) => a + b)
        )
}

export function day1Part1(): number {
    return getCalories()
        .reduce((a, b) => a > b ? a : b)
}

export function day1Part2(): number {
    return getCalories()
        .sort((a, b) => b - a)
        .slice(0, 3)
        .reduce((a, b) => a + b)
}

if (require.main === module) {
    profile(day1Part1)
    profile(day1Part2)
}