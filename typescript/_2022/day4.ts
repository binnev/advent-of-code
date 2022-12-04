import {loadPuzzleInput, profile} from "../utils";

function parseInput(): number[][][] {
    return loadPuzzleInput("2022/day4")
        .split("\n")
        .map(row => row
            .split(",")
            .map(elf => elf
                .split("-")
                .map(n => parseInt(n, 10))
            )
        )
}

function contains([s1, e1]: number[], [s2, e2]: number[]): boolean {
    return (s2 >= s1 && e2 <= e1) || (s1 >= s2 && e1 <= e2)
}

function overlaps([s1, e1]: number[], [s2, e2]: number[]): boolean {
    return (e1 >= s2 && e2 >= s1) || (e2 >= s1 && e1 >= s2)
}

export function day4Part1(): number {
    return parseInput()
        .map(([elf1, elf2]) => contains(elf1, elf2) ? 1 : 0)
        .reduce((a, b) => a + b, 0)
}

export function day4Part2(): number {
    return parseInput()
        .map(([elf1, elf2]) => overlaps(elf1, elf2) ? 1 : 0)
        .reduce((a, b) => a + b, 0)
}

if (require.main === module) {
    profile(day4Part1)
    profile(day4Part2)
}