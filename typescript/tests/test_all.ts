var assert = require('assert')
var _2020 = require("../_2020")
var _2022 = require("../_2022")

describe("2020", () => {
    [
        [_2020.day1Part1, 145875],
        [_2020.day1Part2, 69596112],
    ].forEach(([f, expected]: [() => number, number]) => {
        it(`${f.name}`, () => {
            assert.equal(f(), expected)
        })
    })
})

describe("2022", () => {
    [
        [_2022.day1Part1, 66186],
        [_2022.day1Part2, 196804],
        [_2022.day2Part1, 14264],
        [_2022.day2Part2, 12382],
        [_2022.day3Part1, 8233],
        [_2022.day3Part2, 2821],
    ].forEach(([f, expected]: [() => number, number]) => {
        it(`${f.name}`, () => {
            assert.equal(f(), expected)
        })
    })
})