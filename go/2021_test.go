package main

import (
	"advent/_2021/day1"
	"advent/utils"
	"testing"
)

func Test2021(t *testing.T) {
	cases := []struct {
		f        func() string
		expected string
	}{
		{day1.Part1, "1482"},
		{day1.Part2, "1518"},
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
