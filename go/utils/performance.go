package utils

import (
	"fmt"
	"time"
)

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
