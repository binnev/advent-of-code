package utils

import (
	"fmt"
	"os"
	"reflect"
	"runtime"
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

func Profile(f func() string) {
	t1 := time.Now()
	result := f()
	t2 := time.Now()
	dt := float32(t2.UnixMicro()-t1.UnixMicro()) / 1000000
	funcName := runtime.FuncForPC(reflect.ValueOf(f).Pointer()).Name()
	message := fmt.Sprintf("%v: %v (%.5f seconds)",
		funcName,
		result,
		dt,
	)
	fmt.Println(message)
}
