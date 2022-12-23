package _2022

import (
	"advent/utils"
	"fmt"
	"strings"
)

type Coord = [2]int

func sign(x int) int {
	if x >= 0 {
		return 1
	} else {
		return -1
	}
}

func abs(x int) int {
	if x < 0 {
		return -x
	} else {
		return x
	}
}

func moveHead(head Coord, direction string) Coord {
	switch direction {
	case "R":
		return Coord{head[0] + 1, head[1]}
	case "L":
		return Coord{head[0] - 1, head[1]}
	case "U":
		return Coord{head[0], head[1] - 1}
	case "D":
		return Coord{head[0], head[1] + 1}
	default:
		panic(fmt.Sprintf("Unrecognised direction: %v", direction))
	}
}

func moveTail(head, tail Coord) Coord {
	dx := head[0] - tail[0]
	dy := head[1] - tail[1]

	if abs(dx) > 1 || abs(dy) > 1 {
		newX, newY := tail[0], tail[1]
		if dy != 0 {
			newY = tail[1] + sign(dy)
		}
		if dx != 0 {
			newX = tail[0] + sign(dx)
		}
		return Coord{newX, newY}

	} else {
		return tail
	}
}

func Day9Part1() string {
	input := utils.LoadPuzzleInput("2022/day9")
	head := Coord{} // passing no values results in zero value default
	tail := Coord{}
	tailHistory := map[Coord]int{tail: 1}
	for _, line := range strings.Split(input, "\n") {
		fields := strings.Fields(line)
		direction := fields[0]
		amount := utils.ParseInt(fields[1])
		for ii := 0; ii < amount; ii++ {
			head = moveHead(head, direction)
			tail = moveTail(head, tail)
			tailHistory[tail] = 1
		}

	}
	return fmt.Sprint(len(tailHistory))
}

func Day9Part2() string {
	input := utils.LoadPuzzleInput("2022/day9")
	snake := [10]Coord{} // default values FTW!!
	tail := snake[len(snake)-1]
	tailHistory := map[Coord]int{tail: 1}
	for _, line := range strings.Split(input, "\n") {
		fields := strings.Fields(line)
		direction := fields[0]
		amount := utils.ParseInt(fields[1])
		for ii := 0; ii < amount; ii++ {
			snake[0] = moveHead(snake[0], direction)
			for ii, _ := range snake[1:] {
				snake[ii+1] = moveTail(snake[ii], snake[ii+1])
			}
			tailHistory[snake[len(snake)-1]] = 1
		}
	}
	return fmt.Sprint(len(tailHistory))
}

func Day9() {
	utils.Profile(Day9Part1)
	utils.Profile(Day9Part2)
}
