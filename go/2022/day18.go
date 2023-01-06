package _2022

import (
	"advent/utils"
	"regexp"
	"strings"
)

const (
	LAVA  = '░'
	STEAM = 's'
)

func parseSensors(input string) {
	sensorRx := regexp.MustCompile(`Sensor at x=(\d+), y=(\d+): closest beacon is at x=(\d+), y=(\d+)`)
	for _, line := range strings.Split(input, "\n") {
		match := sensorRx.FindStringSubmatch(line)
		_ = match
		// sensor_x := utils.ParseInt(match[1])
		// sensor_y := utils.ParseInt(match[2])
		// beacon_x := utils.ParseInt(match[3])
		// beacon_y := utils.ParseInt(match[4])
	}
}

func Day18Part1() string {
	return ""
}

func Day18Part2() string {
	return ""
}

func Day18() {
	utils.Profile(Day18Part1)
	utils.Profile(Day18Part2)
}
