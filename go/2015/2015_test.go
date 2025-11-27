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
	})
}
