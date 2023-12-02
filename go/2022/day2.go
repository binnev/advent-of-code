package _2022

import (
	"fmt"
	"strings"
)

const ROCK = 1
const PAPER = 2
const SCISSORS = 3
const LOSE = 1
const DRAW = 2
const WIN = 3

func loadRPSMoves(raw string) [][2]int {
	mapping := map[string]int{
		"A": ROCK,
		"B": PAPER,
		"C": SCISSORS,
		"X": ROCK,
		"Y": PAPER,
		"Z": SCISSORS,
	}
	lines := strings.Split(raw, "\n")
	output := make([][2]int, len(lines))
	for ii, line := range lines {
		chars := strings.Split(line, "")
		l := chars[0]
		r := chars[2]
		output[ii] = [2]int{mapping[string(l)], mapping[string(r)]}
	}
	return output
}

func whoWins(left, right int) int {
	if left == right {
		return -1 // draw
	}
	if left == PAPER && right == ROCK || left == SCISSORS && right == PAPER || left == ROCK && right == SCISSORS {
		return 0 // left wins
	}
	return 1 // right wins
}

func scoreRound(opponent, you int) int {
	points := you
	switch outcome := whoWins(you, opponent); outcome {
	case 0:
		points += 6
	case 1:
		points += 0
	case -1:
		points += 3
	}
	return points
}

func selectMove(opponent, objective int) int {
	switch objective {
	case DRAW:
		return opponent
	case WIN:
		switch opponent {
		case ROCK:
			return PAPER
		case PAPER:
			return SCISSORS
		case SCISSORS:
			return ROCK
		}
	case LOSE:
		switch opponent {
		case ROCK:
			return SCISSORS
		case PAPER:
			return ROCK
		case SCISSORS:
			return PAPER
		}
	}
	return -1
}

func Day2Part1(input string) string {
	rounds := loadRPSMoves(input)
	score := 0
	for _, round := range rounds {
		score += scoreRound(round[0], round[1])
	}
	return fmt.Sprint(score)
}

func Day2Part2(input string) string {
	rounds := loadRPSMoves(input)
	score := 0
	for _, round := range rounds {
		opponent, objective := round[0], round[1]
		you := selectMove(opponent, objective)
		score += scoreRound(opponent, you)
	}
	return fmt.Sprint(score)
}
