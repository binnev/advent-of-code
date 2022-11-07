package days

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"

	"github.com/binnev/advent/utils"
)

func parseLine(line string) (string, string, string, string) {
	rx := regexp.MustCompile(`(?P<a>\d+)-(?P<b>\d+) (?P<c>\w+): (?P<d>\w+)`)
	match := rx.FindStringSubmatch(line)
	a := match[1]
	b := match[2]
	char := match[3]
	pwd := match[4]
	return a, b, char, pwd
}

func Day2Part1() string {
	data := utils.LoadPuzzleInput("day2")
	lines := strings.Split(data, "\n")
	num_valid := 0
	for _, line := range lines {
		a, b, char, pwd := parseLine(line)
		min, _ := strconv.Atoi(a)
		max, _ := strconv.Atoi(b)
		count := strings.Count(pwd, char)
		if min <= count && count <= max {
			num_valid += 1
		}
	}
	return fmt.Sprintf("%v", num_valid)
}

func Day2Part2() string {
	data := utils.LoadPuzzleInput("day2")
	lines := strings.Split(data, "\n")
	num_valid := 0
	for _, line := range lines {
		a, b, char, pwd := parseLine(line)
		index1, _ := strconv.Atoi(a)
		index2, _ := strconv.Atoi(b)
		if (string(pwd[index1-1]) == char) != (string(pwd[index2-1]) == char) {
			num_valid += 1
		}
	}
	return fmt.Sprintf("%v", num_valid)
}

func Day2() {
	utils.Profile(Day2Part1)
	utils.Profile(Day2Part2)
}
