package utils

import (
	"fmt"
	"math"
	"os"
	"reflect"
	"runtime"
	"strconv"
	"strings"
	"time"
)

func LoadPuzzleInput(filename string) string {
	path := fmt.Sprintf("../puzzle_inputs/%v.txt", filename)
	data, err := os.ReadFile(path)
	if err != nil {
		panic(err)
	}
	return string(data)
}

func LoadSolutions(year string) [][]string {
	path := fmt.Sprintf("../solutions/%v.txt", year)
	data, err := os.ReadFile(path)
	if err != nil {
		panic(err)
	}
	lines := strings.Split(string(data), "\n")
	output := [][]string{}
	for _, line := range lines {
		output = append(output, strings.Split(line, ", "))
	}
	return output
}

func GetFuncName[V string | int](f func() V) string {
	return runtime.FuncForPC(reflect.ValueOf(f).Pointer()).Name()
}

func Profile[V string | int](f func() V) V {
	t1 := time.Now()
	result := f()
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
