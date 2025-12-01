package _2015

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"
)

func Day6Part1(input string) string {
	jobs := parse_light_jobs(input)
	grid := LightGrid{}
	for _, job := range jobs {
		grid.change(job.rect, job.action)
	}
	return fmt.Sprint(grid.count())
}

func Day6Part2(input string) string {
	return ""
}

type Rect struct{ x1, y1, x2, y2 int }
type LightAction int
type LightJob struct {
	rect   Rect
	action LightAction
}

const (
	TurnOn LightAction = iota
	TurnOff
	Toggle
)

// [y][x]
type LightGrid [1000][1000]bool

func (grid *LightGrid) change(rect Rect, action LightAction) {
	var value bool
	for y := rect.y1; y <= rect.y2; y++ {
		for x := rect.x1; x <= rect.x2; x++ {
			switch action {
			case TurnOn:
				value = true
			case TurnOff:
				value = false
			case Toggle:
				value = !grid[y][x]
			}
			grid[y][x] = value
		}
	}
}
func (grid LightGrid) count() int {
	count := 0
	for _, line := range grid {
		for _, light := range line {
			if light {
				count++
			}
		}
	}
	return count
}

func parse_light_jobs(input string) []LightJob {
	jobs := []LightJob{}
	for line := range strings.Lines(input) {
		job := LightJob{
			rect:   parse_rect(line),
			action: parse_light_action(line),
		}
		jobs = append(jobs, job)
	}
	return jobs
}

func parse_light_action(line string) LightAction {
	action_rx := regexp.MustCompile(`(turn on|turn off|toggle)`)
	action_str := action_rx.FindStringSubmatch(line)[1]
	switch action_str {
	case "turn on":
		return TurnOn
	case "turn off":
		return TurnOff
	case "toggle":
		return Toggle
	}
	panic(fmt.Sprintf("Couldn't parse action from line: %v", line))
}

func parse_rect(line string) Rect {
	number_rx := regexp.MustCompile(`(\d+)`)
	number_match := number_rx.FindAllStringSubmatch(line, -1)
	x1, _ := strconv.Atoi(number_match[0][1])
	y1, _ := strconv.Atoi(number_match[1][1])
	x2, _ := strconv.Atoi(number_match[2][1])
	y2, _ := strconv.Atoi(number_match[3][1])
	rect := Rect{x1, y1, x2, y2}
	return rect
}
