package _2025

import (
	"advent/utils"
	"fmt"
	"regexp"
	"slices"
	"strconv"
	"strings"
)

/*
I think this one is going to be about bit masks. The target states of the
machines are binary numbers:

	[.##.]   = 0110
	[.###.#] = 011101

Likewise, the button wirings are bit masks:

	(3)   = 0001
	(1,3) = 0101
	(2,3) = 0011

And "pressing a button" translates to "doing a bitwise NOT" (^) between the
button's bitmask and the machine's state.

So, what we want to do is start pressing every combination of buttons, and as
soon as one combination results in the target state, return the number of
buttons pressed.
*/
func Day10Part1(input string) string {
	machines := parse_day10(input)
	total := utils.Sum(utils.Map(calc_fewest_button_presses, machines))
	return fmt.Sprint(total)
}
func Day10Part2(input string) string {
	return ""
}


func calc_fewest_button_presses(machine Machine) int {
	frontier := []int{0} // start with 0b_000... i.e. no buttons pressed
	for ii := 1; ii < 1000; ii++ {
		new_frontier := []int{}
		for _, state := range frontier {
			for _, button := range machine.buttons {
				new_state := state ^ button
				new_frontier = append(new_frontier, new_state)
				if new_state == machine.target_state {
					return ii
				}
			}
		}
		frontier = new_frontier
	}
	panic("Did 1000 iterations and didn't find anything!")
}

func parse_day10(input string) []Machine {
	lines := slices.Collect(strings.Lines(input))
	return utils.Map(parse_machine, lines)
}

func parse_machine(line string) Machine {
	state_rx := regexp.MustCompile(`\[(.+)\]`)
	state_str := state_rx.FindStringSubmatch(line)
	state := parse_target_state(state_str[1])
	state_len := len(state_str[1])

	buttons_rx := regexp.MustCompile(`\(([0-9\,]+)\)`)
	button_matches := buttons_rx.FindAllStringSubmatch(line, -1)
	buttons := []int{}
	for _, button_match := range button_matches {
		button := parse_button(button_match[1], state_len)
		buttons = append(buttons, button)
	}

	joltage_rx := regexp.MustCompile(`\{(.*)\}`)
	joltage_str := joltage_rx.FindStringSubmatch(line)
	joltage_requirements := parse_list_of_ints(joltage_str[1])

	machine := Machine{
		target_state:         int(state),
		buttons:              buttons,
		joltage_requirements: joltage_requirements,
	}

	return machine
}

func parse_target_state(s string) int {
	s = strings.ReplaceAll(s, ".", "0")
	s = strings.ReplaceAll(s, "#", "1")
	state, err := strconv.ParseInt(s, 2, 32)
	if err != nil {
		panic(err)
	}
	return int(state)
}
func parse_list_of_ints(s string) []int {
	parts := strings.Split(s, ",")
	return utils.Map(utils.ParseInt, parts)
}
func parse_button(input string, state_len int) int {
	// Initialise empty bit mask the same length as the target state. So if the
	// target state is "..##..", we initialise "000000". Store it as a list of
	// chars (bytes) so that we can flip individual "bits"
	button_bytes := []byte(strings.Repeat("0", state_len))
	// For each button index in the comma-separated input string, set the bit at
	// that location to 1.
	ints := parse_list_of_ints(input)
	for _, i := range ints {
		button_bytes[i] = '1'
	}

	// Convert the list of chars to a string, and parse it as a base-2 int
	button_str := string(button_bytes)
	button, err := strconv.ParseInt(button_str, 2, 32)
	if err != nil {
		panic(err)
	}
	return int(button)
}

type Machine struct {
	target_state int
	// Each button is a bit mask stored as an int e.g. 0b_0110
	buttons              []int
	joltage_requirements []int
}
