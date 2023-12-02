package _2022

import (
	"advent/utils"
	"regexp"
	"sort"
	"strings"
	"unicode"
)

type Columns map[int]string
type Instruction struct {
	amount int
	orig   int
	dest   int
}

func parseState(stateStr string) Columns {
	state := Columns{}
	rows := strings.Split(stateStr, "\n")
	numberRow := rows[len(rows)-1]
	numCols := len(strings.Fields(numberRow))
	for ii := len(rows) - 2; ii >= 0; ii-- {
		row := rows[ii]
		for col := 0; col < numCols; col++ {
			x := 1 + 4*col
			if len(row) > x {
				char := rune(row[x])
				if !unicode.IsSpace(char) {
					state[col+1] += string(char)
				}
			}
		}
	}
	return state
}

func parseInstructions(instructionsStr string) []Instruction {
	instructionLines := strings.Split(instructionsStr, "\n")
	instructions := make([]Instruction, len(instructionLines))
	rx := regexp.MustCompile(`move (\d+) from (\d+) to (\d+)`)
	for ii, line := range instructionLines {
		match := rx.FindStringSubmatch(line)
		amount := utils.ParseInt(match[1])
		orig := utils.ParseInt(match[2])
		dest := utils.ParseInt(match[3])
		instructions[ii] = Instruction{
			amount: amount,
			orig:   orig,
			dest:   dest,
		}
	}
	return instructions
}

func parseStateInstructions(input string) (Columns, []Instruction) {
	parts := strings.Split(input, "\n\n")
	stateStr, instructionStr := parts[0], parts[1]
	state := parseState(stateStr)
	instructions := parseInstructions(instructionStr)
	return state, instructions
}

func moveCrate(state Columns, i Instruction) {
	index := len(state[i.orig]) - i.amount
	crates := state[i.orig][index:]
	state[i.orig] = state[i.orig][:index]
	state[i.dest] += crates
}

func getTopCrates(state Columns) string {
	var result string
	var cols []int
	for col := range state {
		cols = append(cols, col)
	}
	sort.Ints(cols)
	for _, col := range cols {
		crates, _ := state[col]
		result += string(crates[len(crates)-1])
	}
	return result
}

func Day5Part1(input string) string {
	state, instructions := parseStateInstructions(input)
	for _, instruction := range instructions {
		for ii := 0; ii < instruction.amount; ii++ {
			moveCrate(state, Instruction{
				amount: 1,
				orig:   instruction.orig,
				dest:   instruction.dest,
			})
		}
	}
	return getTopCrates(state)
}

func Day5Part2(input string) string {
	state, instructions := parseStateInstructions(input)
	for _, instruction := range instructions {
		moveCrate(state, instruction)
	}
	return getTopCrates(state)
}
