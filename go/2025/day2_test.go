package _2025

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

const example = `11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124`

func Test_Day2Part1(t *testing.T) {
	assert.Equal(t, "1227775554", Day2Part1(example))
	assert.Equal(t, "33", Day2Part1("11-22"))
}

func Test_is_id_valid(t *testing.T) {
	testcases := []struct {
		input    string
		is_valid bool
	}{
		{"121", true},
		{"1234567890", true},
		{"1212", false},
		{"11", false},
		{"1188511885", false},
	}
	for _, tc := range testcases {
		t.Run(tc.input, func(t *testing.T) {
			assert.Equal(t, tc.is_valid, is_id_valid(tc.input))
		})
	}

}

func Test_get_invalid_ids(t *testing.T) {
	testcases := []struct {
		start, end int
		expected   []int
	}{
		{11, 22, []int{11, 22}},
		{95, 115, []int{99}},
		{998, 1012, []int{1010}},
		{1698522, 1698528, []int{}},
		{1188511880, 1188511890, []int{1188511885}},
		{446443, 446449, []int{446446}},
		{38593856, 38593862, []int{38593859}},
	}
	for _, tc := range testcases {
		description := fmt.Sprintf("%v-%v", tc.start, tc.end)
		t.Run(description, func(t *testing.T) {
			assert.Equal(t, tc.expected, get_invalid_ids(tc.start, tc.end))
		})
	}
}
