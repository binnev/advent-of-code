package main

import (
	"advent/_2020/day1"
	"advent/_2020/day2"
	"advent/utils"
	"testing"
)

func Test2020(t *testing.T) {
	cases := []struct {
		f        func() string
		expected string
	}{
		{day1.Part1, "145875"},
		{day1.Part2, "69596112"},
		{day2.Part1, "628"},
		{day2.Part2, "705"},
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
