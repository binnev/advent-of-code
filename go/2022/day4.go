package _2022

import (
	"advent/utils"
	"fmt"
	"strings"
)

type ElfRange [2]int
type Elves [2]ElfRange

func parseElfRanges(raw string) []Elves {
	lines := strings.Split(raw, "\n")
	elves := make([]Elves, len(lines))
	for rr, row := range strings.Split(raw, "\n") {
		for ee, elf := range strings.Split(row, ",") {
			for ll, limit := range strings.Split(elf, "-") {
				elves[rr][ee][ll] = utils.ParseInt(limit)
			}
		}
	}
	return elves
}

func rangeContains(range1, range2 ElfRange) bool {
	s1, e1 := range1[0], range1[1]
	s2, e2 := range2[0], range2[1]
	return (s2 >= s1 && e2 <= e1) || (s1 >= s2 && e1 <= e2)
}

func rangeOverlaps(range1, range2 ElfRange) bool {
	s1, e1 := range1[0], range1[1]
	s2, e2 := range2[0], range2[1]
	return (e1 >= s2 && e2 >= s1) || (e2 >= s1 && e1 >= s2)
}

func Day4Part1(input string) string {
	score := 0
	for _, ranges := range parseElfRanges(input) {
		if rangeContains(ranges[0], ranges[1]) {
			score += 1
		}
	}
	return fmt.Sprint(score)
}

func Day4Part2(input string) string {
	score := 0
	for _, ranges := range parseElfRanges(input) {
		if rangeOverlaps(ranges[0], ranges[1]) {
			score += 1
		}
	}
	return fmt.Sprint(score)
}
