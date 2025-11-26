package _2015

import (
	. "advent/utils"
	"testing"
)

func Test2015(t *testing.T) {
	RunAdventTestCases(t, []AdventTestCase{
		{Day: "2015/day1", Func: Day1.Part1, Expected: "2015/1/1"},
		{Day: "2015/day1", Func: Day1.Part2, Expected: "2015/1/2"},
	})
}
