package _2025

import (
	"advent/utils"
	"fmt"
	"strings"
)

func Day5Part1(input string) string {
	ranges, ids := parse_day5(input)
	total := 0
	for _, id := range ids {
		if is_fresh(ranges, id) {
			total++
		}
	}
	return fmt.Sprint(total)
}
func Day5Part2(input string) string {
	return ""
}

func is_fresh(ranges []InclusiveRange, id int) bool {
	for _, r := range ranges {
		if r.start <= id && id <= r.end {
			return true
		}
	}
	return false
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

	for line := range strings.Lines(ranges_str) {
		line = strings.TrimSpace(line)
		parts := strings.Split(line, "-")
		start := utils.ParseInt(parts[0])
		end := utils.ParseInt(parts[1])
		r := InclusiveRange{start, end}
		ranges = append(ranges, r)
	}

	return ranges, ids
}

type InclusiveRange struct {
	start, end int
}
