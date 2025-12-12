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
		dial, _ = move_dial(dial, n, dir)
		if dial == 0 {
			zero_count++
		}
	}
	return fmt.Sprint(zero_count)
}

func Day1Part2(input string) string {
	dial := 50
	zero_count := 0
	for line := range strings.Lines(input) {
		dir, n := parse_dial_instruction(line)
		d, c := move_dial(dial, n, dir)
		dial = d
		zero_count += c
	}
	return fmt.Sprint(zero_count)
}

type LeftRight int

const (
	Left LeftRight = iota
	Right
)
const MAX = 100

func move_dial(dial int, n int, dir LeftRight) (int, int) {
	zero_count := 0
	for ii := 0; ii < n; ii++ {
		switch dir {
		case Right:
			dial += 1
			if dial >= MAX {
				dial %= MAX
			}
		case Left:
			if dial > 0 {
				dial -= 1
			} else {
				dial = MAX - 1
			}
		default:
			panic("Bad Direction!")
		}
		if dial == 0 {
			zero_count++
		}
	}
	return dial, zero_count
}

func parse_dial_instruction(line string) (LeftRight, int) {
	line = strings.TrimSpace(line)
	var dir LeftRight
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
