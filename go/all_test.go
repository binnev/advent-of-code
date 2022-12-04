package main

import (
	"advent/_2020"
	"advent/_2021"
	"advent/_2022"
	"advent/utils"
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
