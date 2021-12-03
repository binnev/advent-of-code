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
		return name, errors.New("empty name")
	}

	// message := ... is shorthand for declaring and initialising a variable in one line:
	// var message
	// message = ...
	message := fmt.Sprintf(randomFormat(), name) // I guess this is like str.format in python
	return message, nil
}

// Hellos returns a map that associates each of the named people with a greetings message
// `names []string`: param "names" is type slice with contents string
// `(map[string]string, error)` I'm guessing map[string]string is like {str: str} in python
func Hellos(names []string) (map[string]string, error) {
	messages := make(map[string]string) // make does some kind of instantiation magic

	// loop through the received slice of names, calling the Hello function to get a message for each name.
	for _, name := range names { // I'm guessing range is like enumerate: index and value
		message, err := Hello(name)
		if err != nil {
			return nil, err
		}
		// in the map, associate the retrieved message with the name
		messages[name] = message
	}
	return messages, nil
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
