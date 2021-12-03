package greetings

import (
	"errors"
	"fmt"
	"math/rand"
	"time"
)

// Hello returns a greeting for the named person
// functions that start with a capital letter can be called by functions not in the same package
func Hello(name string) (string, error) {
	// If no name was given, return an error with a message.
	if name == "" {
		return "", errors.New("empty name")
	}

	// message := ... is shorthand for declaring and initialising a variable in one line:
	// var message
	// message = ...
	message := fmt.Sprintf(randomFormat(), name) // I guess this is like str.format in python
	return message, nil
}

// init sets initial values for variables used in the function
// go auto-executes init functions at the program startup, after global variables have been initialised!
func init() {
	rand.Seed(time.Now().UnixNano())
}

// randomFormat returns one of a set of greeting messages. The returned message is selected at random
func randomFormat() string {
	// a slice of message formats -- I think this is equivalent to a python list
	formats := []string{
		"Hi, %v. Welcome!",
		"Great to see you, %v!",
		"Hail, %v! Well met!",
	}

	// return a randomly selected message format by specifying a random index for the slice of formats
	return formats[rand.Intn(len(formats))]
}
