package main

import (
	"fmt"
	"os"
	"testing"
)

func TestAllDays(t *testing.T) {
	// data, err := os.ReadFile("../solutions.txt")
	data, err := os.ReadFile("/home/binnev/code/advent-of-code/_2020/solutions.txt")
	if err != nil {
		panic(err)
	}
	fmt.Println(data)
	fmt.Println(string(data))
	t.Fatalf("boo!")
}
