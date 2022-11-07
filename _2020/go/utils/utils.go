package utils

import (
	"fmt"
	"os"
	"reflect"
	"runtime"
	"time"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func LoadPuzzleInput(filename string) string {
	path := fmt.Sprintf("../puzzle_inputs/%v.txt", filename)
	dat, err := os.ReadFile(path)
	check(err)
	return string(dat)
}

func Profile(a func() string) {
	t1 := time.Now()
	result := a()
	t2 := time.Now()
	dt := float32(t2.UnixMicro()-t1.UnixMicro()) / 1000000
	funcName := runtime.FuncForPC(reflect.ValueOf(a).Pointer()).Name()
	message := fmt.Sprintf("%v: %v (%.5f seconds)",
		funcName,
		result,
		dt,
	)
	fmt.Println(message)
}
