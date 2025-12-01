package _2025

import (
	"fmt"
	"strconv"
	"strings"
)

func Day1Part1(input string) string {
	dial := 50
	zero_count := 0
	for line := range strings.Lines(input) {
		dir, n := parse_dial_instruction(line)
		dial = move_dial(dial, n, MAX, dir)
		if dial == 0 {
			zero_count++
		}
	}
	return fmt.Sprint(zero_count)
}

func Day1Part2(input string) string {
	return ""
}

type Direction int

const (
	Left Direction = iota
	Right
)
const MAX = 100

func move_dial(dial, n, max int, dir Direction) int {
	// Ignore whole rotations and focus on the remainder
	n %= max

	switch dir {
	case Right:
		return (dial + n) % max
	case Left:
		if dial >= n {
			return dial - n
		} else {
			remainder := n - dial
			return max - remainder
		}
	default:
		panic("Bad Direction!")
	}
}

func parse_dial_instruction(line string) (Direction, int) {
	line = strings.TrimSpace(line)
	var dir Direction
	var n int

	dir_str := line[:1]
	switch dir_str {
	case "L":
		dir = Left
	case "R":
		dir = Right
	default:
		panic(fmt.Sprintf("Couldn't parse direction %v", dir_str))
	}

	n_str := line[1:]
	n, err := strconv.Atoi(n_str)
	if err != nil {
		panic(fmt.Sprintf("Couldn't parse int %v", n_str))
	}

	return dir, n
}
