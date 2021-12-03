package greetings

import (
	"errors"
	"fmt"
)

// Hello returns a greeting for the named person
// functions that start with a capital letter can be called by functions not in the same package
func Hello(name string) (string, error) {
	// If no name was given, return an error with a message.
	if name == "" {
		return "", errors.New("empty name")
	}

	// Return a greeting that embeds the name in the message
	// message := ... is shorthand for declaring and initialising a variable in one line:
	// var message
	// message = ...
	message := fmt.Sprintf("Hi, %v. Welcome!", name)
	return message, nil
}
