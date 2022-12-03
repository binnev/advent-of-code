package _2022

import (
	"advent/utils"
	"fmt"
	"strings"
	"unicode"
)

func getPriority(letter rune) int {
	if unicode.IsLower(letter) {
		return int(letter) - 97 + 1
	} else {
		return int(letter) - 65 + 26 + 1
	}
}

func getCommonLetter(words ...string) rune {
	first, rest := words[0], words[1:]
	for _, letter := range first {
		found := true
		for _, word := range rest {
			if !strings.ContainsAny(word, string(letter)) {
				found = false
				break // don't search next word; try next letter instead
			}
		}
		if found {
			return rune(letter)
		}
	}
	return 0
}

func Day3Part1() string {
	input := utils.LoadPuzzleInput("2022/day3")
	elves := strings.Split(input, "\n")
	score := 0
	for _, elf := range elves {
		middle := len(elf) / 2
		left, right := elf[:middle], elf[middle:]
		shared := getCommonLetter(left, right)
		score += getPriority(shared)
	}
	return fmt.Sprint(score)
}

func Day3Part2() string {
	input := utils.LoadPuzzleInput("2022/day3")
	elves := strings.Split(input, "\n")
	score := 0
	for ii := 0; ii < len(elves); ii += 3 {
		elf, second, third := elves[ii], elves[ii+1], elves[ii+2]
		shared := getCommonLetter(elf, second, third)
		score += getPriority(shared)
	}
	return fmt.Sprint(score)
}

func Day3() {
	utils.Profile(Day3Part1)
	utils.Profile(Day3Part2)
}
