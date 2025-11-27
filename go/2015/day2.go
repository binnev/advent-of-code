package _2015

import (
	"fmt"
	"slices"
	"strconv"
	"strings"
)

func Day2Part1(input string) string {
	total := 0
	for _, dimensions := range parse_day2(input) {
		l := dimensions[0]
		w := dimensions[1]
		h := dimensions[2]
		total += calculate_wrapping_paper(l, w, h)
	}
	return fmt.Sprint(total)
}

func Day2Part2(input string) string {
	total := 0
	for _, dimensions := range parse_day2(input) {
		l := dimensions[0]
		w := dimensions[1]
		h := dimensions[2]
		total += calculate_ribbon(l, w, h)
	}
	return fmt.Sprint(total)
}

func calculate_wrapping_paper(l, w, h int) int {
	area := 2*l*w + 2*w*h + 2*h*l
	sides := []int{l, w, h}
	slices.Sort(sides)
	smallest_side_area := sides[0] * sides[1]
	return area + smallest_side_area
}

func calculate_ribbon(l, w, h int) int {
	sides := []int{l, w, h}
	slices.Sort(sides)
	smallest_perim := (sides[0] + sides[1]) * 2
	bow := l * w * h
	return smallest_perim + bow
}

func parse_day2(input string) [][3]int {
	out := [][3]int{}
	for line := range strings.Lines(input) {
		lwh := strings.Split(strings.TrimSpace(line), "x")
		l, _ := strconv.Atoi(lwh[0])
		w, _ := strconv.Atoi(lwh[1])
		h, _ := strconv.Atoi(lwh[2])
		out = append(out, [3]int{l, w, h})
	}
	return out
}
