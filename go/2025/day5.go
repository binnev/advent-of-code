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
	ranges, _ := parse_day5(input)
	ranges = merge_ranges(ranges)
	total := 0
	for _, r := range ranges {
		total += r.len()
	}
	return fmt.Sprint(total)
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

func (r InclusiveRange) String() string {
	return fmt.Sprintf("%v..%v", r.start, r.end)
}

var _ fmt.Stringer = (*InclusiveRange)(nil)

func (r InclusiveRange) overlaps(other InclusiveRange) bool {
	return (r.start <= other.end && other.start <= r.end)
}
func (r *InclusiveRange) merge(other InclusiveRange) {
	if !r.overlaps(other) {
		panic(fmt.Sprintf(
			"Can't merge ranges that don't overlap: %v, %v",
			r,
			other,
		))
	}
	start := utils.Min([]int{r.start, other.start})
	end := utils.Max([]int{r.end, other.end})
	r.start = start
	r.end = end
}
func (r InclusiveRange) len() int {
	return r.end - r.start + 1
}

func merge_ranges(ranges []InclusiveRange) []InclusiveRange {
	out := map[InclusiveRange]bool{}
	for _, r := range ranges {
		// Get the indexes of existing output ranges that overlap with the
		// current range. Remove them from the output set.
		overlapping := []InclusiveRange{}
		for other := range out {
			if other.overlaps(r) {
				delete(out, other)
				overlapping = append(overlapping, other)
			}
		}

		n_overlaps := len(overlapping)
		switch n_overlaps {

		// If zero overlap, append the current range to the output.
		case 0:
			out[r] = true

		// If more than 1 overlaps, panic, because I can't be bothered to implement merging multiple ranges unless I need to.
		default:
			// Merge the overlapping ranges into the current range, and insert it into the out
			for _, other := range overlapping {
				r.merge(other)
			}
			out[r] = true
		}
	}
	out_arr := []InclusiveRange{}
	for r := range out {
		out_arr = append(out_arr, r)
	}
	return out_arr
}
