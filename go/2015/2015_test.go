package _2015

import (
	. "advent/utils"
	"testing"
)

func Test2015(t *testing.T) {
	RunAdventTestCases(t, []AdventTestCase{
		{Day: "2015/day1", Func: Day1Part1, Expected: ""},
		{Day: "2015/day1", Func: Day1Part2, Expected: ""},
	})
}
