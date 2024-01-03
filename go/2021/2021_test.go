package _2021

import (
	. "advent/utils"
	"testing"
)

func Test2021(t *testing.T) {
	RunAdventTestCases(t, []AdventTestCase{
		{Day: "2021/day1", Func: Day1Part1, Expected: "1482"},
		{Day: "2021/day1", Func: Day1Part2, Expected: "1518"},
	})
}
