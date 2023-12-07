package utils

import (
	"fmt"
	"log"
	"math"
	"os"
	"path"
	"reflect"
	"runtime"
	"strconv"
	"strings"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

type AdventFunc func(string) string
type AdventTestCase struct {
	Day      string
	Func     AdventFunc
	Expected string
}

// I use this logic to parametrize all the year testcases, so here it is
// encapsulated in a function
func RunAdventTestCases(t *testing.T, testcases []AdventTestCase) {
	for _, tc := range testcases {
		raw := LoadPuzzleInput(tc.Day)
		t.Run(GetFuncName(tc.Func), func(t *testing.T) {
			result := Profile(tc.Func, raw)
			assert.Equal(t, tc.Expected, result)
		})
	}
}

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

func GetFuncName(f AdventFunc) string {
	return runtime.FuncForPC(reflect.ValueOf(f).Pointer()).Name()
}

func Wrap(f AdventFunc) AdventFunc {
	wrapped := func(raw string) string {
		return Profile(f, raw)
	}
	return wrapped
}

func Profile(f AdventFunc, raw string) string {
	t1 := time.Now()
	result := f(raw)
	t2 := time.Now()
	dt := float32(t2.UnixMicro()-t1.UnixMicro()) / 1000000
	message := fmt.Sprintf("%v: %v (%.5f seconds)",
		GetFuncName(f),
		result,
		dt,
	)
	fmt.Println(message)
	return result
}

func ParseInt(s string) int {
	output, err := strconv.Atoi(s)
	if err != nil {
		panic(err)
	}
	return output
}

func Sum[V int | float64](arr []V) V {
	var sum V
	for _, item := range arr {
		sum += item
	}
	return sum
}

func Max[V int | float64](arr []V) V {
	if len(arr) == 0 {
		panic("Can't do max of empty array")
	}
	max := math.Inf(-1)
	for _, item := range arr {
		floated := float64(item)
		if floated > max {
			max = floated
		}
	}
	return V(max)
}

func Min[V int | float64](arr []V) V {
	if len(arr) == 0 {
		panic("Can't do min of empty array")
	}
	min := math.Inf(1)
	for _, item := range arr {
		floated := float64(item)
		if floated < min {
			min = floated
		}
	}
	return V(min)
}

func Contains[V int | string](arr []V, value V) bool {
	for _, item := range arr {
		if item == value {
			return true
		}
	}
	return false
}

func Reverse[AnySlice ~[]A, A any](arr AnySlice) {
	reversed := make(AnySlice, len(arr))
	length := len(arr)
	for ii, value := range arr {
		reversed[length-1-ii] = value
	}
	copy(arr, reversed)
}

func Map[I any, O any](f func(I) O, arr []I) []O {
	result := make([]O, len(arr))
	for ii, item := range arr {
		result[ii] = f(item)
	}
	return result
}
