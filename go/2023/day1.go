package _2023

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"
)

func Day1Part1(raw string) string {
	raw = strings.TrimSpace(raw)
	rx := regexp.MustCompile(`(\d)`)
	result := 0
	for _, line := range strings.Split(raw, "\n") {
		digits := rx.FindAll([]byte(line), -1)
		first := string(digits[0])
		last := string(digits[len(digits)-1])
		number, _ := strconv.Atoi(first + last)
		result += number
	}
	return fmt.Sprint(result)
}

func regexMagic(s string) []string {
	rx := regexp.MustCompile(`^(one|two|three|four|five|six|seven|eight|nine|[1-9])`)
	matches := []string{}
	length := len(s)
	for ii := 0; ii < length; ii++ {
		substr := s[ii:length]
		if rx.MatchString(substr) {

			match := rx.FindString(substr)
			matches = append(matches, string(match))
		}
	}
	return matches
}

func Day1Part2(raw string) string {
	digit_map := map[string]string{
		"one":   "1",
		"two":   "2",
		"three": "3",
		"four":  "4",
		"five":  "5",
		"six":   "6",
		"seven": "7",
		"eight": "8",
		"nine":  "9",
	}
	raw = strings.TrimSpace(raw)
	result := 0
	for _, line := range strings.Split(raw, "\n") {
		digit_strings := regexMagic(line)
		first := digit_strings[0]
		last := digit_strings[len(digit_strings)-1]
		if d, ok := digit_map[first]; ok {
			first = d
		}
		if d, ok := digit_map[last]; ok {
			last = d
		}
		number, _ := strconv.Atoi(first + last)
		result += number
	}
	return fmt.Sprint(result)
}
