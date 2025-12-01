package _2025

import (
	. "advent/utils"
	"testing"
)

func Test2025(t *testing.T) {
	RunAdventTestCases(t, []AdventTestCase{
		{Day: "2025/day1", Func: Day1Part1, Expected: "964"},
		{Day: "2025/day1", Func: Day1Part2, Expected: ""},
	})
}
