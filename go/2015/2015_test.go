package _2015

import (
	. "advent/utils"
	"testing"
)

func Test2015(t *testing.T) {
	RunAdventTestCases(t, []AdventTestCase{
		{Day: "2015/day1", Func: Day1Part1, Expected: "74"},
		{Day: "2015/day1", Func: Day1Part2, Expected: "1795"},
		{Day: "2015/day2", Func: Day2Part1, Expected: "1606483"},
		{Day: "2015/day2", Func: Day2Part2, Expected: "3842356"},
		{Day: "2015/day3", Func: Day3Part1, Expected: "2565"},
		{Day: "2015/day3", Func: Day3Part2, Expected: "2639"},
		{Day: "2015/day4", Func: Day4Part1, Expected: "282749"},
		{Day: "2015/day4", Func: Day4Part2, Expected: "9962624"},
		{Day: "2015/day5", Func: Day5Part1, Expected: "255"},
	})
}
