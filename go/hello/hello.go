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

	// Get a greeting message and print it
	message, err := greetings.Hello("Gladys")
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(message)
}
