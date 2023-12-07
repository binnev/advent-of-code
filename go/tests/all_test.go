package tests

import (
	_2020 "advent/2020"
	_2021 "advent/2021"
	_2022 "advent/2022"
	_2023 "advent/2023"
	"advent/utils"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

type AdventTestCase struct {
	day      string
	f        utils.AdventFunc
	expected string
}

// I use this logic to parametrize all the year testcases, so here it is
// encapsulated in a function
func RunAdventTestCases(t *testing.T, testcases []AdventTestCase) {
	for _, tc := range testcases {
		raw := utils.LoadPuzzleInput(tc.day)
		t.Run(utils.GetFuncName(tc.f), func(t *testing.T) {
			result := utils.Profile(tc.f, raw)
			assert.Equal(t, tc.expected, result)
		})
	}
}

func Test2020(t *testing.T) {
	RunAdventTestCases(t, []AdventTestCase{
		{"2020/day1", _2020.Day1Part1, "145875"},
		{"2020/day1", _2020.Day1Part2, "69596112"},
		{"2020/day2", _2020.Day2Part1, "628"},
		{"2020/day2", _2020.Day2Part2, "705"},
	})
}

func Test2021(t *testing.T) {
	RunAdventTestCases(t, []AdventTestCase{
		{"2021/day1", _2021.Day1Part1, "1482"},
		{"2021/day1", _2021.Day1Part2, "1518"},
	})
}

func Test2022(t *testing.T) {
	RunAdventTestCases(t, []AdventTestCase{
		{"2022/day1", _2022.Day1Part1, "66186"},
		{"2022/day1", _2022.Day1Part2, "196804"},
		{"2022/day2", _2022.Day2Part1, "14264"},
		{"2022/day2", _2022.Day2Part2, "12382"},
		{"2022/day3", _2022.Day3Part1, "8233"},
		{"2022/day3", _2022.Day3Part2, "2821"},
		{"2022/day4", _2022.Day4Part1, "567"},
		{"2022/day4", _2022.Day4Part2, "907"},
		{"2022/day5", _2022.Day5Part1, "GRTSWNJHH"},
		{"2022/day5", _2022.Day5Part2, "QLFQDBBHM"},
		{"2022/day6", _2022.Day6Part1, "1175"},
		{"2022/day6", _2022.Day6Part2, "3217"},
		{"2022/day7", _2022.Day7Part1, "1792222"},
		{"2022/day7", _2022.Day7Part2, "1112963"},
		{"2022/day8", _2022.Day8Part1, "1698"},
		{"2022/day8", _2022.Day8Part2, "672280"},
		{"2022/day9", _2022.Day9Part1, "6494"},
		{"2022/day9", _2022.Day9Part2, "2691"},
		{"2022/day10", _2022.Day10Part1, "13440"},
		{"2022/day10", _2022.Day10Part2, strings.Join([]string{
			"###  ###  ####  ##  ###   ##  ####  ##  ",
			"#  # #  #    # #  # #  # #  #    # #  # ",
			"#  # ###    #  #    #  # #  #   #  #  # ",
			"###  #  #  #   # ## ###  ####  #   #### ",
			"#    #  # #    #  # # #  #  # #    #  # ",
			"#    ###  ####  ### #  # #  # #### #  # ",
		}, "\n")},
		{"2022/day11", _2022.Day11Part1, "64032"},
		{"2022/day11", _2022.Day11Part2, "12729522272"},
		{"2022/day12", _2022.Day12Part1, "440"},
		{"2022/day12", _2022.Day12Part2, "439"},
		{"2022/day13", _2022.Day13Part1, "6420"},
		{"2022/day13", _2022.Day13Part2, "22000"},
		{"2022/day14", _2022.Day14Part1, "755"},
		{"2022/day14", _2022.Day14Part2, "29805"},
		{"2022/day17", _2022.Day17Part1, "3109"},
		// {"2022/day17", _2022.Day17Part2, "1541449275365"},
	})
}

func Test2023(t *testing.T) {
	RunAdventTestCases(t, []AdventTestCase{
		{"2023/day1", _2023.Day1Part1, "55123"},
		{"2023/day1", _2023.Day1Part2, "55260"},
		{"2023/day2", _2023.Day2Part1, "1853"},
	})
}
