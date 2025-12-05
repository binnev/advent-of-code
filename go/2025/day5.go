package _2025

import (
	"advent/utils"
	"strings"
)

func Day5Part1(input string) string {

	return ""
}
func Day5Part2(input string) string {
	return ""
}

func parse_day5(input string) ([]InclusiveRange, []int) {
	ranges := []InclusiveRange{}
	ids := []int{}

	parts := strings.Split(input, "\n\n")
	ranges_str := parts[0]
	ids_str := parts[1]
	for line := range strings.Lines(ids_str) {
		line = strings.TrimSpace(line)
		id := utils.ParseInt(line)
		ids = append(ids, id)
	}

	return ranges, ids
}

type InclusiveRange struct {
	start, end int
}
