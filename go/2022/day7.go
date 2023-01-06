package _2022

import (
	"advent/utils"
	"fmt"
	"strings"
)

type Filesystem map[string]int

func cd(cwd, dirName string) string {
	switch dirName {
	case "..":
		parts := strings.Split(cwd, "/")
		cwd = strings.Join(parts[:len(parts)-1], "/")
	case "/":
		cwd = ""
	default:
		cwd = cwd + "/" + dirName
	}
	return cwd
}

func exploreFolders(input string) Filesystem {
	root := ""
	cwd := root
	contents := Filesystem{"/": 0}

	for _, line := range strings.Split(input, "\n") {
		if strings.HasPrefix(line, "$") {
			// parse commands
			cmd := strings.Replace(line, "$ ", "", -1)
			if strings.HasPrefix(cmd, "cd") {
				dirName := strings.Replace(cmd, "cd ", "", -1)
				cwd = cd(cwd, dirName)
			}
		} else {
			// parse ls contents
			if strings.HasPrefix(line, "dir") {
				dirName := strings.Replace(line, "dir ", "", -1)
				contents[cwd+"/"+dirName] = 0
			} else {
				split := strings.Fields(line)
				fileSize := split[0]
				fileName := split[1]
				fs := utils.ParseInt(fileSize)
				contents[cwd+"/"+fileName] = fs
			}
		}
	}
	return contents
}

func getFolderSize(contents Filesystem, folderPath string) int {
	total := 0
	for path, size := range contents {
		if strings.HasPrefix(path, folderPath) && !strings.HasSuffix(path, folderPath) {
			total += size
		}
	}
	return total
}

func Day7Part1() string {
	input := utils.LoadPuzzleInput("2022/day7")
	contents := exploreFolders(input)
	total := 0
	for path, size := range contents {
		if size == 0 {
			folderSize := getFolderSize(contents, path)
			if folderSize < 100000 {
				total += folderSize
			}
		}
	}
	return fmt.Sprint(total)
}

func Day7Part2() string {
	input := utils.LoadPuzzleInput("2022/day7")
	contents := exploreFolders(input)
	totalSpace := 70000000
	requiredSpace := 30000000
	occupiedSpace := getFolderSize(contents, "/")
	unusedSpace := totalSpace - occupiedSpace
	needToDelete := requiredSpace - unusedSpace

	allSizes := []int{}
	for path, size := range contents {
		if size == 0 {
			folderSize := getFolderSize(contents, path)
			allSizes = append(allSizes, folderSize)
		}
	}
	smallest := 9999999999
	for _, folderSize := range allSizes {
		if folderSize >= needToDelete && folderSize < smallest {
			smallest = folderSize
		}
	}
	return fmt.Sprint(smallest)
}

func Day7() {
	utils.Profile(Day7Part1)
	utils.Profile(Day7Part2)
}
