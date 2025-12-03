package _2025

import (
	. "advent/utils"
	"testing"
)

func Test2025(t *testing.T) {
	RunAdventTestCases(t, []AdventTestCase{
		{Day: "2025/day1", Func: Day1Part1, Expected: "964"},
		{Day: "2025/day1", Func: Day1Part2, Expected: "5872"},
		{Day: "2025/day2", Func: Day2Part1, Expected: "21898734247"},
		{Day: "2025/day2", Func: Day2Part2, Expected: "28915664389"},
		{Day: "2025/day3", Func: Day3Part1, Expected: "17493"},
	})
}
