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
	relative_file_path := fmt.Sprintf("../../../.puzzle-inputs/%v.txt", filename)
	file_path := path.Join(current_file, relative_file_path)

	data, err := os.ReadFile(file_path)
	if err != nil {
		log.Fatal(err)
	}
	return strings.TrimSpace(string(data))
}
