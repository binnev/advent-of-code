var assert = require('assert')
var _2020 = require("../_2020")

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