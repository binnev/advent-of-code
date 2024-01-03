package _2020

import (
	. "advent/utils"
	"testing"
)

func Test2020(t *testing.T) {
	RunAdventTestCases(t, []AdventTestCase{
		{Day: "2020/day1", Func: Day1Part1, Expected: "145875"},
		{Day: "2020/day1", Func: Day1Part2, Expected: "69596112"},
		{Day: "2020/day2", Func: Day2Part1, Expected: "628"},
		{Day: "2020/day2", Func: Day2Part2, Expected: "705"},
	})
}
