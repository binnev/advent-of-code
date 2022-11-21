package main

import (
	"advent/_2021"
	"advent/utils"
	"testing"
)

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
