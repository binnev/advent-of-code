package _2022

import (
	"advent/utils"
	"fmt"
	"strings"
)

type HeightMap map[Coord]int

func getHeight(char rune) int {
	// S = start (same height as 'a')
	// E = end (same height as 'z')
	if char == 'S' {
		char = 'a'
	}
	if char == 'E' {
		char = 'z'
	}
	return int(char) - 97
}

func getHeightMap(input string) (HeightMap, Coord, Coord) {
	heightMap := HeightMap{}
	var start, target Coord
	for y, characters := range strings.Split(input, "\n") {
		for x, char := range characters {
			coord := Coord{x, y}
			heightMap[coord] = getHeight(char)
			if char == 'S' {
				start = coord
			}
			if char == 'E' {
				target = coord
			}
		}
	}
	return heightMap, start, target
}

func getNeighbours(heightMap HeightMap, pos Coord, reverse bool) []Coord {
	x, y := pos[0], pos[1]
	height := heightMap[pos]
	candidates := []Coord{
		{x + 1, y},
		{x - 1, y},
		{x, y + 1},
		{x, y - 1},
	}
	var neighbours []Coord
	for _, neighbour := range candidates {
		neighbourHeight, ok := heightMap[neighbour]
		if !ok {
			continue
		}
		condition := neighbourHeight > height
		if reverse {
			condition = neighbourHeight < height
		}
		if condition {
			if abs(neighbourHeight-height) < 2 {
				neighbours = append(neighbours, neighbour)
			}
		} else {
			neighbours = append(neighbours, neighbour)
		}
	}
	return neighbours
}

func getNeighboursUphill(heightMap HeightMap, pos Coord) []Coord {
	return getNeighbours(heightMap, pos, false)
}

func getNeighboursDownhill(heightMap HeightMap, pos Coord) []Coord {
	return getNeighbours(heightMap, pos, true)
}

func BFS(
	grid HeightMap,
	start Coord,
	getNeighboursFunc func(HeightMap, Coord) []Coord,
) HeightMap {
	visited := map[Coord]bool{}
	distances := HeightMap{start: 0}
	frontier := map[Coord]bool{start: true}
	neighbourDist := 1
	for {
		neighbours := map[Coord]bool{}
		for node := range frontier {
			for _, neighbour := range getNeighboursFunc(grid, node) {
				if !visited[neighbour] {
					neighbours[neighbour] = true
				}
			}
		}
		if len(neighbours) == 0 {
			break // explored whole map
		}
		for n := range neighbours {
			dist, ok := distances[n]
			if !ok {
				dist = 9999
			}
			dist = utils.Min([]int{dist, neighbourDist})
			distances[n] = dist
		}
		for node := range frontier {
			visited[node] = true
		}
		frontier = neighbours // wrong type
		neighbourDist++
	}
	return distances
}

func Day12Part1() string {
	input := utils.LoadPuzzleInput("2022/day12")
	heightMap, start, target := getHeightMap(input)
	distances := BFS(heightMap, start, getNeighboursUphill)
	return fmt.Sprint(distances[target])
}

func Day12Part2() string {
	input := utils.LoadPuzzleInput("2022/day12")
	HeightMap, _, target := getHeightMap(input)
	distances := BFS(HeightMap, target, getNeighboursDownhill)
	lowPoints := []Coord{}
	for coord, height := range HeightMap {
		if height == 0 {
			lowPoints = append(lowPoints, coord)
		}
	}
	results := []int{}
	for _, point := range lowPoints {
		dist, ok := distances[point]
		if ok {
			results = append(results, dist)
		}
	}
	return fmt.Sprint(utils.Min(results))
}
