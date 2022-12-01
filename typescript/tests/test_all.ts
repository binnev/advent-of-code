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
    ].forEach(([f, expected]: [() => number, number]) => {
        it(`${f.name}`, () => {
            assert.equal(f(), expected)
        })
    })
})