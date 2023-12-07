package _2022

import (
	. "advent/utils"
	"strings"
	"testing"
)

func Test2022(t *testing.T) {
	RunAdventTestCases(t, []AdventTestCase{
		{Day: "2022/day1", Func: Day1Part1, Expected: "66186"},
		{Day: "2022/day1", Func: Day1Part2, Expected: "196804"},
		{Day: "2022/day2", Func: Day2Part1, Expected: "14264"},
		{Day: "2022/day2", Func: Day2Part2, Expected: "12382"},
		{Day: "2022/day3", Func: Day3Part1, Expected: "8233"},
		{Day: "2022/day3", Func: Day3Part2, Expected: "2821"},
		{Day: "2022/day4", Func: Day4Part1, Expected: "567"},
		{Day: "2022/day4", Func: Day4Part2, Expected: "907"},
		{Day: "2022/day5", Func: Day5Part1, Expected: "GRTSWNJHH"},
		{Day: "2022/day5", Func: Day5Part2, Expected: "QLFQDBBHM"},
		{Day: "2022/day6", Func: Day6Part1, Expected: "1175"},
		{Day: "2022/day6", Func: Day6Part2, Expected: "3217"},
		{Day: "2022/day7", Func: Day7Part1, Expected: "1792222"},
		{Day: "2022/day7", Func: Day7Part2, Expected: "1112963"},
		{Day: "2022/day8", Func: Day8Part1, Expected: "1698"},
		{Day: "2022/day8", Func: Day8Part2, Expected: "672280"},
		{Day: "2022/day9", Func: Day9Part1, Expected: "6494"},
		{Day: "2022/day9", Func: Day9Part2, Expected: "2691"},
		{Day: "2022/day10", Func: Day10Part1, Expected: "13440"},
		{Day: "2022/day10", Func: Day10Part2, Expected: strings.Join([]string{
			"###  ###  ####  ##  ###   ##  ####  ##  ",
			"#  # #  #    # #  # #  # #  #    # #  # ",
			"#  # ###    #  #    #  # #  #   #  #  # ",
			"###  #  #  #   # ## ###  ####  #   #### ",
			"#    #  # #    #  # # #  #  # #    #  # ",
			"#    ###  ####  ### #  # #  # #### #  # ",
		}, "\n")},
		{Day: "2022/day11", Func: Day11Part1, Expected: "64032"},
		{Day: "2022/day11", Func: Day11Part2, Expected: "12729522272"},
		{Day: "2022/day12", Func: Day12Part1, Expected: "440"},
		{Day: "2022/day12", Func: Day12Part2, Expected: "439"},
		{Day: "2022/day13", Func: Day13Part1, Expected: "6420"},
		{Day: "2022/day13", Func: Day13Part2, Expected: "22000"},
		{Day: "2022/day14", Func: Day14Part1, Expected: "755"},
		{Day: "2022/day14", Func: Day14Part2, Expected: "29805"},
		{Day: "2022/day17", Func: Day17Part1, Expected: "3109"},
		// {"2022/day17", Day17Part2, "1541449275365"},
	})
}
