package main

import (
	"advent/days"
	"fmt"
	"os"
	"testing"
)

func TestAllDays(t *testing.T) {
	data, err := os.ReadFile("../solutions.txt")
	if err != nil {
		panic(err)
	}
	fmt.Println(data)
	fmt.Println(string(data))
	result := days.Day1Part1()
	fmt.Println(result)
	t.Fatalf("at least the tests are running!!")
}
