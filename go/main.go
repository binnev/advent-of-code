package main

import (
	_2015 "advent/2015"
	_2025 "advent/2025"
	"advent/utils"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	// Define command-line arguments for year and day
	// TODO these have to be passed as -flags, can't be passed as positionals
	input := os.Args[1]
	parts := strings.Split(input, "/")
	fmt.Println(parts)
	if len(parts) < 3 {
		panic(fmt.Sprintf("Didn't get enough input! Expected year/day/part, got %v", input))
	}
	year, err := strconv.Atoi(parts[0])
	if err != nil {
		panic(fmt.Sprintf("Failed to parse year from %v", year))
	}
	day, err := strconv.Atoi(parts[1])
	if err != nil {
		panic(fmt.Sprintf("Failed to parse day from %v", day))
	}
	part, err := strconv.Atoi(parts[2])
	if err != nil {
		panic(fmt.Sprintf("Failed to parse part from %v", part))
	}

	// Get the solution func
	key := [3]int{year, day, part}
	fn, ok := REGISTRY[key]
	if !ok {
		msg := fmt.Sprintf("No registry entry for %d day %d part %d", year, day, part)
		panic(msg)
	}
	// Load the puzzle input
	input_path := fmt.Sprintf("%d/day%d", year, day)
	puzzle_input := utils.LoadPuzzleInput(input_path)

	// Profile and execute the puzzle
	utils.Profile(fn, puzzle_input)
}

var REGISTRY = map[[3]int]utils.AdventFunc{
	// 2015
	{2015, 1, 1}: _2015.Day1Part1,
	{2015, 1, 2}: _2015.Day1Part2,
	{2015, 2, 1}: _2015.Day2Part1,
	{2015, 2, 2}: _2015.Day2Part2,
	{2015, 3, 1}: _2015.Day3Part1,
	{2015, 3, 2}: _2015.Day3Part2,
	{2015, 4, 1}: _2015.Day4Part1,
	{2015, 4, 2}: _2015.Day4Part2,
	{2015, 5, 1}: _2015.Day5Part1,
	{2015, 5, 2}: _2015.Day5Part2,
	{2015, 6, 1}: _2015.Day6Part1,
	{2015, 6, 2}: _2015.Day6Part2,

	// 2025
	{2025, 1, 1}: _2025.Day1Part1,
	{2025, 1, 2}: _2025.Day1Part2,
	{2025, 2, 1}: _2025.Day2Part1,
	{2025, 2, 2}: _2025.Day2Part2,
	{2025, 3, 1}: _2025.Day3Part1,
	{2025, 3, 2}: _2025.Day3Part2,
	{2025, 4, 1}: _2025.Day4Part1,
	{2025, 4, 2}: _2025.Day4Part2,
	{2025, 5, 1}: _2025.Day5Part1,
	{2025, 5, 2}: _2025.Day5Part2,
	{2025, 6, 1}: _2025.Day6Part1,
	{2025, 6, 2}: _2025.Day6Part2,
	{2025, 7, 1}: _2025.Day7Part1,
	{2025, 7, 2}: _2025.Day7Part2,
	{2025, 8, 1}: _2025.Day8Part1,
	{2025, 8, 2}: _2025.Day8Part2,
}
