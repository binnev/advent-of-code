package main

import (
	"advent/_2020"
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
