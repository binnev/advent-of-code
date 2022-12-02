package _2022

import (
	"advent/utils"
	"fmt"
	"strings"
)

const ROCK = 1
const PAPER = 2
const SCISSORS = 3
const LOSE = 1
const DRAW = 2
const WIN = 3

func loadRPSMoves() [][2]int {
	mapping := map[string]int{
		"A": ROCK,
		"B": PAPER,
		"C": SCISSORS,
		"X": ROCK,
		"Y": PAPER,
		"Z": SCISSORS,
	}
	input := utils.LoadPuzzleInput("2022/day2")
	lines := strings.Split(input, "\n")
	output := [][2]int{}
	for _, line := range lines {
		chars := strings.Split(line, "")
		l := chars[0]
		r := chars[2]
		output = append(output, [2]int{mapping[string(l)], mapping[string(r)]})
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
	// switch objective {
	// case DRAW:
	// 	return opponent
	// case WIN:
	// 	if opponent == ROCK {
	// 		return PAPER
	// 	}
	// 	if opponent == PAPER {
	// 		return SCISSORS
	// 	}
	// 	if opponent == SCISSORS {
	// 		return ROCK
	// 	}
	// case LOSE:
	// 	if opponent == ROCK {
	// 		return SCISSORS
	// 	}
	// 	if opponent == PAPER {
	// 		return ROCK
	// 	}
	// 	if opponent == SCISSORS {
	// 		return PAPER
	// 	}
	// default:
	// 	return -1
	// }
	output := -1
	if objective == DRAW {
		output = opponent
	} else if objective == WIN {
		if opponent == ROCK {
			output = PAPER
		}
		if opponent == PAPER {
			output = SCISSORS
		}
		if opponent == SCISSORS {
			output = ROCK
		}
	} else if objective == LOSE {
		if opponent == ROCK {
			output = SCISSORS
		}
		if opponent == PAPER {
			output = ROCK
		}
		if opponent == SCISSORS {
			output = PAPER
		}
	}
	return output
}

func Day2Part1() string {
	rounds := loadRPSMoves()
	score := 0
	for _, round := range rounds {
		score += scoreRound(round[0], round[1])
	}
	return fmt.Sprint(score)
}

func Day2Part2() string {
	rounds := loadRPSMoves()
	score := 0
	for _, round := range rounds {
		opponent, objective := round[0], round[1]
		you := selectMove(opponent, objective)
		score += scoreRound(opponent, you)
	}
	return fmt.Sprint(score)
}

func Day2() {
	utils.Profile(Day2Part1)
	utils.Profile(Day2Part2)
}
