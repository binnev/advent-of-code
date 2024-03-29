package _2022

import (
	"advent/utils"
	"fmt"
	"regexp"
	"sort"
	"strings"
)

const (
	ADD    = 0
	MULT   = 1
	SQUARE = 2
)

type Operation [2]int
type Monkey struct {
	id        int
	divisor   int
	ifFalse   int
	ifTrue    int
	count     int
	inventory []int
	operation Operation
}
type MonkeyBunch map[int]*Monkey // * means pointer to a monkey

const monkeyRx = `Monkey (\d):
  Starting items: (.*)
  Operation: new = (.*)
  Test: divisible by (\d+)
    If true: throw to monkey (\d)
    If false: throw to monkey (\d)`

func parseOperation(operationStr string) Operation {
	operationStr = strings.TrimSpace(operationStr)
	rxSquare := regexp.MustCompile(`old \* old`)
	rxMult := regexp.MustCompile(`old \* (\d+)`)
	rxAdd := regexp.MustCompile(`old \+ (\d+)`)

	if rxSquare.MatchString(operationStr) {
		return Operation{SQUARE, 69}
	} else if rxMult.MatchString(operationStr) {
		match := rxMult.FindStringSubmatch(operationStr)
		number := utils.ParseInt(match[1])
		return Operation{MULT, number}
	} else if rxAdd.MatchString(operationStr) {
		match := rxAdd.FindStringSubmatch(operationStr)
		number := utils.ParseInt(match[1])
		return Operation{ADD, number}
	} else {
		panic(fmt.Sprintf("Help! Couldn't find any match for: '%v'", operationStr))
	}
}

func parseMonkey(monkeyStr string) Monkey {
	rx := regexp.MustCompile(monkeyRx)
	match := rx.FindStringSubmatch(monkeyStr)

	id := utils.ParseInt(match[1])
	itemsStr := match[2]
	items := []int{}
	for _, item := range strings.Split(itemsStr, ", ") {
		items = append(items, utils.ParseInt(item))
	}
	operationStr := match[3]
	divisor := utils.ParseInt(match[4])
	ifTrue := utils.ParseInt(match[5])
	ifFalse := utils.ParseInt(match[6])

	operation := parseOperation(operationStr)
	return Monkey{
		id:        id,
		operation: operation,
		ifTrue:    ifTrue,
		ifFalse:   ifFalse,
		divisor:   divisor,
		inventory: items,
	}
}

func ParseMonkeys(input string) MonkeyBunch {
	monkeyBunch := MonkeyBunch{}
	for id, monkeyStr := range strings.Split(input, "\n\n") {
		monkey := parseMonkey(monkeyStr)
		monkeyBunch[id] = &monkey
	}
	return monkeyBunch
}

func monkeyThrow(monkeyId int, item int, others MonkeyBunch, decreaseWorry func(int) int) {
	monkey := others[monkeyId]
	number := monkey.operation[1]
	switch monkey.operation[0] {
	case SQUARE:
		item *= item
	case MULT:
		item *= number
	case ADD:
		item += number
	}
	item = decreaseWorry(item)
	otherId := monkey.ifFalse
	if item%monkey.divisor == 0 {
		otherId = monkey.ifTrue
	}
	others[otherId].inventory = append(others[otherId].inventory, item)
	monkey.count++
}

func getMostActiveMonkeys(monkeys MonkeyBunch, top int) []Monkey {
	sortedMonkeys := []Monkey{}
	for _, monkeyPtr := range monkeys {
		sortedMonkeys = append(sortedMonkeys, *monkeyPtr)
	}
	sort.Slice(
		sortedMonkeys,
		func(i, j int) bool {
			return sortedMonkeys[i].count > sortedMonkeys[j].count
		},
	)
	return sortedMonkeys[:top]
}

func Day11Part1(input string) string {
	monkeys := ParseMonkeys(input)
	worryFunc := func(number int) int { return number / 3 }
	for round := 0; round < 20; round++ {
		for monkeyId := 0; monkeyId < len(monkeys); monkeyId++ {
			monkey := monkeys[monkeyId]
			for _, item := range monkey.inventory {
				monkeyThrow(monkeyId, item, monkeys, worryFunc)
			}
			monkey.inventory = []int{}
		}
	}
	top2 := getMostActiveMonkeys(monkeys, 2)
	result := top2[0].count * top2[1].count
	return fmt.Sprint(result)
}

func Day11Part2(input string) string {
	monkeys := ParseMonkeys(input)
	modulus := 1
	for _, monkey := range monkeys {
		modulus *= monkey.divisor
	}
	worryFunc := func(number int) int { return number % modulus }
	for round := 0; round < 10000; round++ {
		for monkeyId := 0; monkeyId < len(monkeys); monkeyId++ {
			monkey := monkeys[monkeyId]
			for _, item := range monkey.inventory {
				monkeyThrow(monkeyId, item, monkeys, worryFunc)
			}
			monkey.inventory = []int{}
		}
	}
	top2 := getMostActiveMonkeys(monkeys, 2)
	result := top2[0].count * top2[1].count
	return fmt.Sprint(result)
}
