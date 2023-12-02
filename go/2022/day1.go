package _2022

import (
	"advent/utils"
	"fmt"
	"sort"
	"strings"
)

func getCalories(raw string) []int {
	elves := strings.Split(raw, "\n\n")
	calories := make([]int, len(elves))
	for ii, elf := range elves {
		elfCalories := 0
		for _, s := range strings.Split(elf, "\n") {
			elfCalories += utils.ParseInt(s)
		}
		calories[ii] = elfCalories
	}
	return calories
}

func Day1Part1(input string) string {
	maxCalories := utils.Max(getCalories(input))
	return fmt.Sprint(maxCalories)
}

func Day1Part2(input string) string {
	calories := getCalories(input)
	sort.Slice(
		calories,
		func(a, b int) bool { return calories[a] > calories[b] },
	)
	sum := utils.Sum(calories[:3])
	return fmt.Sprint(sum)
}
