package day2

import (
	"advent/utils"
	"fmt"
	"regexp"
	"strings"
)

type RgbTuple struct {
	red   int
	green int
	blue  int
}

type Game struct {
	number int
	hands  []RgbTuple
}

func Part1(input string) string {
	limit := RgbTuple{red: 12, green: 13, blue: 14}
	result := 0
	games := parse_games(input)
	for _, game := range games {
		if is_game_possible(game.hands, limit) {
			result += game.number
		}
	}
	return fmt.Sprint(result)
}

func Part2(input string) string {
	games := parse_games(input)
	result := 0
	for _, game := range games {
		min_cubes := get_min_cubes(game.hands)
		power := min_cubes.red * min_cubes.blue * min_cubes.green
		result += power
	}
	return fmt.Sprint(result)
}

func get_min_cubes(hands []RgbTuple) RgbTuple {
	minimum := RgbTuple{red: 0, green: 0, blue: 0}
	for _, hand := range hands {
		if hand.red > minimum.red {
			minimum.red = hand.red
		}
		if hand.blue > minimum.blue {
			minimum.blue = hand.blue
		}
		if hand.green > minimum.green {
			minimum.green = hand.green
		}
	}
	return minimum
}

func parse_games(input string) []Game {
	lines := strings.Split(strings.TrimSpace(input), "\n")
	return utils.Map(parse_game, lines)
}

func parse_game(input string) Game {
	var rx *regexp.Regexp

	rx = regexp.MustCompile(`Game (\d+): (.*)`)
	match := rx.FindStringSubmatch(input)
	game := utils.ParseInt(match[1])
	rest := match[2]

	cube_groups := utils.Map(strings.TrimSpace, strings.Split(rest, ";"))

	rx = regexp.MustCompile(`(\d+) (blue|red|green)`)
	cube_colours := []RgbTuple{}
	for _, group := range cube_groups {
		rgb := RgbTuple{}
		matches := rx.FindAllStringSubmatch(group, -1)
		for _, match := range matches {
			number := utils.ParseInt(match[1])
			color := match[2]
			switch color {
			case "red":
				rgb.red = number
			case "green":
				rgb.green = number
			case "blue":
				rgb.blue = number
			}
		}
		cube_colours = append(cube_colours, rgb)
	}
	return Game{game, cube_colours}
}

func is_game_possible(hands []RgbTuple, limit RgbTuple) bool {
	for _, hand := range hands {
		if hand.red > limit.red || hand.blue > limit.blue || hand.green > limit.green {
			return false
		}
	}
	return true
}
