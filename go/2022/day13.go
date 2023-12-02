package _2022

import (
	"advent/utils"
	"fmt"
	"regexp"
	"sort"
	"strings"
)

const (
	UNORDERED = -1
	UNKNOWN   = 0
	ORDERED   = 1
)

var rxNumeric = regexp.MustCompile(`^\d+$`)

func parseDay13Input(input string) [][2]string {
	output := [][2]string{}
	for _, packetPair := range strings.Split(input, "\n\n") {
		lines := strings.Split(packetPair, "\n")
		left, right := lines[0], lines[1]
		output = append(output, [2]string{left, right})
	}
	return output
}

func readList(str string, start int) (string, int) {
	depth := 1
	ii := start + 1
	for depth > 0 {
		switch str[ii] {
		case '[':
			depth++
		case ']':
			depth--
		}
		ii++
	}
	result := str[start:ii]
	return result, ii
}

func readNumber(str string, start int) (string, int) {
	ii := start
	for ii < len(str) {
		char := str[ii]
		if !rxNumeric.Match([]byte{char}) {
			break
		}
		ii++
	}
	result := str[start:ii]
	return result, ii
}

func readValues(str string) []string {
	str = str[1 : len(str)-1]
	values := []string{}
	ii := 0
	var value string
	length := len(str)
	for ii < length {
		char := str[ii]
		if rxNumeric.Match([]byte{char}) {
			value, ii = readNumber(str, ii)
			values = append(values, value)
		} else if char == '[' {
			value, ii = readList(str, ii)
			values = append(values, value)
		} else {
			ii++
		}
	}
	return values
}

func arePacketsOrdered(left, right string) int {
	// early exit
	if left == right {
		return UNKNOWN
	}

	// both ints
	if rxNumeric.MatchString(left) && rxNumeric.MatchString(right) {
		lNum := utils.ParseInt(left)
		rNum := utils.ParseInt(right)
		if lNum < rNum {
			return ORDERED
		} else if lNum == rNum {
			return UNKNOWN
		} else {
			return UNORDERED
		}
	}

	// mixed types
	if rxNumeric.MatchString(left) && !rxNumeric.MatchString(right) {
		return arePacketsOrdered(fmt.Sprintf("[%v]", left), right)
	}
	if rxNumeric.MatchString(right) && !rxNumeric.MatchString(left) {
		return arePacketsOrdered(left, fmt.Sprintf("[%v]", right))
	}

	// both list
	leftValues := readValues(left)
	rightValues := readValues(right)
	leftIsShorter := UNKNOWN
	if len(leftValues) < len(rightValues) {
		leftIsShorter = ORDERED
	} else if len(leftValues) > len(rightValues) {
		leftIsShorter = UNORDERED
	}
	for {
		if len(leftValues) == 0 || len(rightValues) == 0 {
			return leftIsShorter
		}
		leftVal := leftValues[0]
		leftValues = leftValues[1:]
		rightVal := rightValues[0]
		rightValues = rightValues[1:]

		result := arePacketsOrdered(leftVal, rightVal)
		if result == UNKNOWN {
			continue
		} else {
			return result
		}
	}
}

func Day13Part1(input string) string {
	packets := parseDay13Input(input)
	score := 0
	for ii, packetPair := range packets {
		left, right := packetPair[0], packetPair[1]
		result := arePacketsOrdered(left, right)
		if result == ORDERED {
			score += ii + 1
		}
	}
	return fmt.Sprint(score)
}

func Day13Part2(input string) string {
	input = strings.Replace(input, "\n\n", "\n", -1)
	input += "\n[[2]]\n[[6]]"
	packets := strings.Split(input, "\n")
	sort.Slice(
		packets,
		func(i, j int) bool {
			left := packets[i]
			right := packets[j]
			result := arePacketsOrdered(left, right)
			return result == ORDERED
		},
	)
	var loc2 int
	var loc6 int
	for ii, value := range packets {
		if value == "[[2]]" {
			loc2 = ii + 1
		}
		if value == "[[6]]" {
			loc6 = ii + 1
		}
	}
	return fmt.Sprint(loc2 * loc6)
}
