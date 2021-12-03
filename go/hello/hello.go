// code executed as an application must be in a main package. I guess this is like in python when you do:
// if __name__ == "__main__": runstuff()
package main

import (
	"example.com/greetings"
	"fmt"
	"log"
)

func main() {
	// Set properties of the predefined Logger, including
	// the log entry prefix and a flag to disable printing
	// the time, source file, and line number
	log.SetPrefix("greetings: ")
	log.SetFlags(0)
	// a slice of names
	names := []string{"Gladys", "Samantha", "Darrin"}

	// Get a greeting message and print it
	messages, err := greetings.Hellos(names)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(messages)
}
