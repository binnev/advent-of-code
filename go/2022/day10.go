package _2022

import (
	"advent/utils"
	"fmt"
	"strings"
)

func Day10Part1() string {
	input := utils.LoadPuzzleInput("2022/day10")
	code := strings.Split(input, "\n")
	tasks := []int{}
	x := 1
	cycle := 0
	signal := 0
	for len(code) > 0 || len(tasks) > 0 {
		cycle++
		if utils.Contains([]int{20, 60, 100, 140, 180, 220}, cycle) {
			signal += cycle * x
		}
		if len(tasks) > 0 {
			end := len(tasks) - 1
			x += tasks[end]
			tasks = tasks[:end]
		} else {
			line := code[0]
			code = code[1:]
			if strings.HasPrefix(line, "addx") {
				split := strings.Split(line, " ")
				amount := split[1]
				tasks = append(tasks, utils.ParseInt(amount))
			}
		}
	}
	return fmt.Sprint(signal)
}
