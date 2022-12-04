import {loadPuzzleInput, profile} from "../utils";

type ElfRange = number[]
type Elves = ElfRange[]

function parseInput(): Elves[] {
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

function contains([s1, e1]: ElfRange, [s2, e2]: ElfRange): boolean {
    return (s2 >= s1 && e2 <= e1) || (s1 >= s2 && e1 <= e2)
}

function overlaps([s1, e1]: ElfRange, [s2, e2]: ElfRange): boolean {
    return (e1 >= s2 && e2 >= s1) || (e2 >= s1 && e1 >= s2)
}

export function day4Part1(): number {
    return parseInput().filter(([elf1, elf2]) => contains(elf1, elf2)).length
}

export function day4Part2(): number {
    return parseInput().filter(([elf1, elf2]) => overlaps(elf1, elf2)).length
}

if (require.main === module) {
    profile(day4Part1)
    profile(day4Part2)
}