package utils

import (
	"reflect"
	"runtime"
	"testing"

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

func GetFuncName(f AdventFunc) string {
	return runtime.FuncForPC(reflect.ValueOf(f).Pointer()).Name()
}
