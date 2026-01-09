package _2025

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

const example_day10 = `[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
`

func Test_Day10Part2(t *testing.T) {
	result := Day10Part2(example_day10)
	assert.Equal(t, "33", result)
}

func Test_Day10Part1(t *testing.T) {
	result := Day10Part1(example_day10)
	assert.Equal(t, "7", result)
}

func Test_bitwise_not_works_as_expected(t *testing.T) {
	target := 0b_0110
	initial := 0b_0
	button := 0b_110
	result := initial ^ button
	assert.Equal(t, target, result)
}

func Test_parse_target_state(t *testing.T) {
	testcases := []struct {
		s        string
		expected State
	}{
		{".", State{0}},
		{"#", State{1}},
		{".##.", State{0, 1, 1, 0}},
		{".###.#", State{0, 1, 1, 1, 0, 1}},
	}
	for _, tc := range testcases {
		t.Run(tc.s, func(t *testing.T) {
			result := parse_target_state(tc.s)
			assert.Equal(t, tc.expected, result)
		})
	}
}

func Test_parse_list_of_ints(t *testing.T) {
	s := "0,1,2,3,4"
	expected := []int{0, 1, 2, 3, 4}
	result := parse_list_of_ints(s)
	assert.Equal(t, expected, result)
}

func Test_parse_machine(t *testing.T) {
	testcases := []struct {
		input    string
		expected Machine
	}{
		{
			"[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}",
			Machine{
				target_state: State{0, 1, 1, 1, 0, 1},
				buttons: []Button{
					{0, 1, 2, 3, 4},
					{0, 3, 4},
					{0, 1, 2, 4, 5},
					{1, 2},
				},
				joltage_requirements: []int{10, 11, 11, 5, 10, 5},
			},
		},
	}
	for _, tc := range testcases {
		t.Run(tc.input, func(t *testing.T) {
			machine := parse_machine(tc.input)
			assert.Equal(t, tc.expected, machine)
		})
	}
}

func Test_calc_fewest_button_presses(t *testing.T) {
	testcases := []struct {
		machine_str string
		expected    int
	}{
		{
			"[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}",
			2,
		},
		{
			"[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}",
			3,
		},
		{
			"[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}",
			2,
		},
	}
	for _, tc := range testcases {
		t.Run(tc.machine_str, func(t *testing.T) {
			machine := parse_machine(tc.machine_str)
			result := calc_fewest_button_presses(machine)
			assert.Equal(t, tc.expected, result)
		})
	}
}
