package _2022

import (
	"advent/utils"
	"fmt"
	"strings"
)

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
	x, y := head[0], head[1]
	switch direction {
	case "R":
		return Coord{x + 1, y}
	case "L":
		return Coord{x - 1, y}
	case "U":
		return Coord{x, y - 1}
	case "D":
		return Coord{x, y + 1}
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

func Day9Part1(input string) string {
	head := Coord{}
	tail := Coord{}
	tailHistory := map[Coord]bool{tail: true}
	for _, line := range strings.Split(input, "\n") {
		fields := strings.Fields(line)
		direction := fields[0]
		amount := utils.ParseInt(fields[1])
		for ii := 0; ii < amount; ii++ {
			head = moveHead(head, direction)
			tail = moveTail(head, tail)
			tailHistory[tail] = true
		}
	}
	return fmt.Sprint(len(tailHistory))
}

func Day9Part2(input string) string {
	snake := [10]Coord{}
	tail := snake[len(snake)-1]
	tailHistory := map[Coord]bool{tail: true}
	for _, line := range strings.Split(input, "\n") {
		fields := strings.Fields(line)
		direction := fields[0]
		amount := utils.ParseInt(fields[1])
		for ii := 0; ii < amount; ii++ {
			snake[0] = moveHead(snake[0], direction)
			for ii := range snake[1:] {
				snake[ii+1] = moveTail(snake[ii], snake[ii+1])
			}
			tailHistory[snake[len(snake)-1]] = true
		}
	}
	return fmt.Sprint(len(tailHistory))
}
