package _2022

import (
	"advent/utils"
	"fmt"
	"sort"
	"strconv"
	"strings"
)

func getCalories() []int {
	data := utils.LoadPuzzleInput("2022/day1")
	elves := strings.Split(data, "\n\n")
	calories := []int{}
	for _, elf := range elves {
		elfCalories := 0
		for _, s := range strings.Split(elf, "\n") {
			c, _ := strconv.Atoi(s)
			elfCalories += c
		}
		calories = append(calories, elfCalories)
	}
	return calories
}

func Day1Part1() string {
	maxCalories := 0
	for _, calories := range getCalories() {
		if calories > maxCalories {
			maxCalories = calories
		}
	}
	return fmt.Sprint(maxCalories)
}

func Day1Part2() string {
	calories := getCalories()
	sort.Slice(
		calories,
		func(a, b int) bool {
			return calories[a] > calories[b]
		},
	)
	sum := 0
	for ii := 0; ii < 3; ii++ {
		sum += calories[ii]
	}
	return fmt.Sprint(sum)
}

func Day1() {
	utils.Profile(Day1Part1)
	utils.Profile(Day1Part2)
}
