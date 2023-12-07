package day2

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

var example = `Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green`

func TestPart1(t *testing.T) {
	result := Part1(example)
	assert.Equal(t, "8", result)
}

func TestPart2(t *testing.T) {
	assert.Equal(t, "2286", Part2(example))
}

func Test_parse_game(t *testing.T) {
	input := "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue"
	game := parse_game(input)
	assert.Equal(t, 2, game.number)
	assert.Equal(t, []RgbTuple{
		{blue: 1, green: 2, red: 0},
		{green: 3, blue: 4, red: 1},
		{green: 1, blue: 1, red: 0},
	}, game.hands)
}
