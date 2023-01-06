package main

import (
	_2020 "advent/2020"
	_2021 "advent/2021"
	_2022 "advent/2022"
	"advent/utils"
	"strings"
	"testing"
)

func Test2020(t *testing.T) {
	cases := []struct {
		f        func() string
		expected string
	}{
		{_2020.Day1Part1, "145875"},
		{_2020.Day1Part2, "69596112"},
		{_2020.Day2Part1, "628"},
		{_2020.Day2Part2, "705"},
	}

	for _, tc := range cases {
		t.Run(utils.GetFuncName(tc.f), func(t *testing.T) {
			result := tc.f()
			if result != tc.expected {
				t.Fatalf("%v failed; got %v; expected %v",
					utils.GetFuncName(tc.f),
					result,
					tc.expected,
				)
			}
		})

	}
}

func Test2021(t *testing.T) {
	cases := []struct {
		f        func() string
		expected string
	}{
		{_2021.Day1Part1, "1482"},
		{_2021.Day1Part2, "1518"},
	}

	for _, tc := range cases {
		t.Run(utils.GetFuncName(tc.f), func(t *testing.T) {
			result := tc.f()
			if result != tc.expected {
				t.Fatalf("%v failed; got %v; expected %v",
					utils.GetFuncName(tc.f),
					result,
					tc.expected,
				)
			}
		})

	}
}

func Test2022(t *testing.T) {
	cases := []struct {
		f        func() string
		expected string
	}{
		{_2022.Day1Part1, "66186"},
		{_2022.Day1Part2, "196804"},
		{_2022.Day2Part1, "14264"},
		{_2022.Day2Part2, "12382"},
		{_2022.Day3Part1, "8233"},
		{_2022.Day3Part2, "2821"},
		{_2022.Day4Part1, "567"},
		{_2022.Day4Part2, "907"},
		{_2022.Day5Part1, "GRTSWNJHH"},
		{_2022.Day5Part2, "QLFQDBBHM"},
		{_2022.Day6Part1, "1175"},
		{_2022.Day6Part2, "3217"},
		{_2022.Day7Part1, "1792222"},
		{_2022.Day7Part2, "1112963"},
		{_2022.Day8Part1, "1698"},
		{_2022.Day8Part2, "672280"},
		{_2022.Day9Part1, "6494"},
		{_2022.Day9Part2, "2691"},
		{_2022.Day10Part1, "13440"},
		{_2022.Day10Part2, strings.Join([]string{
			"###  ###  ####  ##  ###   ##  ####  ##  ",
			"#  # #  #    # #  # #  # #  #    # #  # ",
			"#  # ###    #  #    #  # #  #   #  #  # ",
			"###  #  #  #   # ## ###  ####  #   #### ",
			"#    #  # #    #  # # #  #  # #    #  # ",
			"#    ###  ####  ### #  # #  # #### #  # ",
		}, "\n")},
		{_2022.Day11Part1, "64032"},
		{_2022.Day11Part2, "12729522272"},
		{_2022.Day12Part1, "440"},
		{_2022.Day12Part2, "439"},
		{_2022.Day14Part1, "755"},
		{_2022.Day14Part2, "29805"},
	}

	for _, tc := range cases {
		t.Run(utils.GetFuncName(tc.f), func(t *testing.T) {
			result := tc.f()
			if result != tc.expected {
				t.Fatalf("%v failed; got %v; expected %v",
					utils.GetFuncName(tc.f),
					result,
					tc.expected,
				)
			}
		})
	}
}
