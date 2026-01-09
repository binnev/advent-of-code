package _2025

import (
	"advent/utils"
	"fmt"
	"regexp"
	"slices"
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

// Same story, but instead of bitwise NOT we increment the relevant counters.
// Instead of parsing the buttons as ints, we must parse them as tuples of ints.
// In fact we can probably use the same approach for part 1 -.-
func Day10Part2(input string) string {
	machines := parse_day10(input)
	total := utils.Sum(utils.Map(calc_fewest_button_presses_joltage, machines))
	return fmt.Sprint(total)
}

func calc_fewest_button_presses(machine Machine) int {
	initial := make(State, len(machine.target_state))
	frontier := []State{initial}
	MAX := 1000
	for ii := 1; ii < MAX; ii++ {
		new_frontier := []State{}
		for _, state := range frontier {
			for _, button := range machine.buttons {
				new := state.apply(button)
				new_frontier = append(new_frontier, new)
				if slices.Equal(new, machine.target_state) {
					return ii
				}
			}
		}
		frontier = new_frontier
	}
	panic("Did MAX iterations and didn't find anything!")
}

type Container struct {
	joltages        Joltages
	pressed_buttons []Button
}

func (c Container) apply(button Button) Container {
	new := Container{
		c.joltages.apply(button),
		c.pressed_buttons,
	}
	new.pressed_buttons = append(new.pressed_buttons, button)
	return new
}

func calc_fewest_button_presses_joltage(machine Machine) int {
	initial := make(Joltages, len(machine.joltage_requirements))
	pressed_buttons := []Button{}
	frontier := []Container{{initial, pressed_buttons}}
	MAX := 2
	for ii := 1; ii < MAX; ii++ {
		utils.Print("Frontier len %v", len(frontier))
		new_frontier := []Container{}
		for _, container := range frontier {
			for _, button := range machine.buttons {
				for _, pressed := range container.pressed_buttons {
					if slices.Equal(pressed, button) {
						continue
					} else {
						utils.Print("Pressed %v != %v", pressed, button)
					}
				}
				new := container.apply(button)
				new_frontier = append(new_frontier, new)
				if slices.Equal(new.joltages, machine.joltage_requirements) {
					return ii
				}
			}
		}
		frontier = new_frontier
	}
	panic("Did MAX iterations and didn't find anything!")
}

func parse_day10(input string) []Machine {
	lines := slices.Collect(strings.Lines(input))
	return utils.Map(parse_machine, lines)
}

func parse_machine(line string) Machine {
	state_rx := regexp.MustCompile(`\[(.+)\]`)
	state_str := state_rx.FindStringSubmatch(line)
	state := parse_target_state(state_str[1])

	buttons_rx := regexp.MustCompile(`\(([0-9\,]+)\)`)
	button_matches := buttons_rx.FindAllStringSubmatch(line, -1)
	buttons := []Button{}
	for _, button_match := range button_matches {
		button := parse_list_of_ints(button_match[1])
		buttons = append(buttons, button)
	}

	joltage_rx := regexp.MustCompile(`\{(.*)\}`)
	joltage_str := joltage_rx.FindStringSubmatch(line)
	joltage_requirements := parse_list_of_ints(joltage_str[1])

	machine := Machine{
		target_state:         state,
		buttons:              buttons,
		joltage_requirements: joltage_requirements,
	}

	return machine
}

func parse_target_state(input string) State {
	s := State{}
	for _, char := range input {
		if char == '#' {
			s = append(s, 1)
		} else {
			s = append(s, 0)
		}
	}
	return s
}
func parse_list_of_ints(s string) []int {
	parts := strings.Split(s, ",")
	return utils.Map(utils.ParseInt, parts)
}

type State []int

func (s State) apply(button Button) State {
	new := make(State, len(s))
	copy(new, s)
	for _, wire := range button {
		if new[wire] == 0 {
			new[wire] = 1
		} else {
			new[wire] = 0
		}
	}
	return new
}

type Joltages []int

func (j Joltages) apply(button Button) Joltages {
	new := make(Joltages, len(j))
	copy(new, j)
	for _, wire := range button {
		new[wire]++
	}
	return new
}

type Button []int
type Machine struct {
	target_state State
	// Each button is a bit mask stored as an int e.g. 0b_0110
	buttons              []Button
	joltage_requirements []int
}
