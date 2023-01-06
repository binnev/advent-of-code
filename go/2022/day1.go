package _2022

import (
	"advent/utils"
	"fmt"
	"sort"
	"strings"
)

func getCalories() []int {
	data := utils.LoadPuzzleInput("2022/day1")
	elves := strings.Split(data, "\n\n")
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

func Day1Part1() string {
	maxCalories := utils.Max(getCalories())
	return fmt.Sprint(maxCalories)
}

func Day1Part2() string {
	calories := getCalories()
	sort.Slice(
		calories,
		func(a, b int) bool { return calories[a] > calories[b] },
	)
	sum := utils.Sum(calories[:3])
	return fmt.Sprint(sum)
}

func Day1() {
	utils.Profile(Day1Part1)
	utils.Profile(Day1Part2)
}
