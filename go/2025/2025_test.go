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
		{Day: "2025/day3", Func: Day3Part2, Expected: "173685428989126"},
		{Day: "2025/day4", Func: Day4Part1, Expected: "1508"},
		{Day: "2025/day4", Func: Day4Part2, Expected: "8538"},
		{Day: "2025/day5", Func: Day5Part1, Expected: "888"},
		{Day: "2025/day5", Func: Day5Part2, Expected: "344378119285354"},
		{Day: "2025/day6", Func: Day6Part1, Expected: "5361735137219"},
		{Day: "2025/day6", Func: Day6Part2, Expected: "11744693538946"},
		{Day: "2025/day7", Func: Day7Part1, Expected: "1687"},
		{Day: "2025/day7", Func: Day7Part2, Expected: "390684413472684"},
	})
}
