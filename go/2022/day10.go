package _2022

import (
	"advent/utils"
	"fmt"
	"strings"
)

func iterateBeam(tasks *[]int, code *[]string) int {
	amount := 0
	if len(*tasks) > 0 {
		end := len(*tasks) - 1
		amount = (*tasks)[end]
		*tasks = (*tasks)[:end]
	} else if len(*code) > 0 {
		line := (*code)[0]
		*code = (*code)[1:]
		if strings.HasPrefix(line, "addx") {
			fields := strings.Fields(line)
			amountStr := fields[1]
			*tasks = append(*tasks, utils.ParseInt(amountStr))
		}
	}
	return amount
}

func Day10Part1(input string) string {
	code := strings.Split(input, "\n")
	tasks := []int{}
	x := 1
	signal := 0
	for cycle := 1; cycle <= 220; cycle++ {
		if utils.Contains([]int{20, 60, 100, 140, 180, 220}, cycle) {
			signal += cycle * x
		}
		x += iterateBeam(&tasks, &code)
	}
	return fmt.Sprint(signal)
}

func Day10Part2(input string) string {
	code := strings.Split(input, "\n")
	tasks := []int{}
	x := 1
	screen := SparseMatrix{}
	for cycle := 0; cycle < 240; cycle++ {
		row := cycle / 40
		pixelX := cycle % 40
		pixel := ' '
		if x-1 <= pixelX && pixelX <= x+1 {
			pixel = '#'
		}
		screen[Coord{pixelX, row}] = pixel
		x += iterateBeam(&tasks, &code)
	}
	return screen.ToString(false, 0, '.')
}
