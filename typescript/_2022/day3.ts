import {loadPuzzleInput, profile} from "../utils";


function getPriority(letter: string): number {
    if (letter.toLowerCase() === letter) {
        return letter.codePointAt(0) - 97 + 1
    } else {
        return letter.codePointAt(0) - 65 + 26 + 1
    }
}

function getCommonLetter(...words: string[]): string {
    let [first, ...rest] = words
    for (const letter of Array.from(first)) {
        let found = true
        for (const word of rest) {
            if (!word.includes(letter)) {
                found = false
                break
            }
        }
        if (found) {
            return letter
        }
    }
    return ""
}

export function day3Part1(): number {
    const input = loadPuzzleInput("2022/day3")
    const elves = input.split("\n")
    let score = 0
    for (const elf of elves) {
        const middle = elf.length / 2
        const [left, right] = [elf.slice(0, middle), elf.slice(middle, elf.length)]
        const shared = getCommonLetter(left, right)
        score += getPriority(shared)
    }
    return score
}

export function day3Part2(): number {
    const input = loadPuzzleInput("2022/day3")
    const elves = input.split("\n")
    let score = 0
    for (let ii = 0; ii < elves.length; ii += 3) {
        const [elf, second, third] = elves.slice(ii, ii + 3)
        const shared = getCommonLetter(elf, second, third)
        score += getPriority(shared)
    }
    return score
}

if (require.main === module) {
    profile(day3Part1)
    profile(day3Part2)
}