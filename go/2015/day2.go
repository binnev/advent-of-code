package _2015

import (
	"fmt"
	"slices"
	"strconv"
	"strings"
)

func Day2Part1(input string) string {
	total := 0
	for line := range strings.Lines(input) {
		lwh := strings.Split(strings.TrimSpace(line), "x")
		l, _ := strconv.Atoi(lwh[0])
		w, _ := strconv.Atoi(lwh[1])
		h, _ := strconv.Atoi(lwh[2])
		paper := calculate_wrapping_paper(l, w, h)
		total += paper
	}
	return fmt.Sprint(total)
}
func Day2Part2(input string) string {
	return ""
}

func calculate_wrapping_paper(l, w, h int) int {
	area := 2*l*w + 2*w*h + 2*h*l
	sides := []int{l, w, h}
	slices.Sort(sides)
	smallest_side_area := sides[0] * sides[1]
	return area + smallest_side_area
}
