package utils

import (
	"fmt"
	"log"
	"os"
	"path"
	"runtime"
	"strings"
)

func LoadPuzzleInput(filename string) string {
	// Need to explicitly locate the file relative to the current file, because
	// using a relative path results in different results when running the tests
	// and running main.go
	_, current_file, _, _ := runtime.Caller(0)
	relative_file_path := fmt.Sprintf("../../../_inputs/%v.txt", filename)
	file_path := path.Join(current_file, relative_file_path)

	data, err := os.ReadFile(file_path)
	if err != nil {
		log.Fatal(err)
	}
	return string(data)
}

func LoadSolutions(year string) [][]string {
	_, current_file, _, _ := runtime.Caller(0)
	relative_file_path := fmt.Sprintf("../../../_solutions/%v.txt", year)
	file_path := path.Join(current_file, relative_file_path)
	data, err := os.ReadFile(file_path)
	if err != nil {
		log.Fatal(err)
	}
	lines := strings.Split(string(data), "\n")
	output := [][]string{}
	for _, line := range lines {
		output = append(output, strings.Split(line, ", "))
	}
	return output
}
