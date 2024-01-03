package _2023

import (
	. "advent/utils"
	"testing"

	"advent/2023/day1"
	"advent/2023/day2"
)

func Test2023(t *testing.T) {
	RunAdventTestCases(t, []AdventTestCase{
		{Day: "2023/day1", Func: day1.Part1, Expected: "55123"},
		{Day: "2023/day1", Func: day1.Part2, Expected: "55260"},
		{Day: "2023/day2", Func: day2.Part1, Expected: "1853"},
		{Day: "2023/day2", Func: day2.Part2, Expected: "72706"},
	})
}
