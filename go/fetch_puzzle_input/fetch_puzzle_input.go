package main

import (
	"advent/utils"
	"context"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/go-resty/resty/v2"
	"golang.org/x/sync/semaphore"
)

const INPUTS_DIR = "../.puzzle-inputs"
const FIRST_YEAR = 2015
const CONCURRENT_REQUESTS = 3

type Job struct {
	year int
	day  int
}

func main() {
	cookie := load_session_cookie()

	client := resty.New()
	client.SetHeader("Cookie", fmt.Sprintf("session=%s", cookie))

	sem := semaphore.NewWeighted(CONCURRENT_REQUESTS)
	ctx := context.TODO()

	jobs := calculate_years_and_days()
	for _, job := range jobs {
		rate_limited(job.year, job.day, client, sem, ctx)
	}

	if err := sem.Acquire(ctx, CONCURRENT_REQUESTS); err != nil {
		log.Fatal("Failed to wait for tasks to finish")
	}
}

func rate_limited(
	year, day int,
	client *resty.Client,
	sem *semaphore.Weighted,
	ctx context.Context,
) {
	if err := sem.Acquire(ctx, 1); err != nil {
		panic("Couldn't acquire semaphore!")
	}
	// Spawn background goroutine which releases the semaphore when it's done
	go func() {
		defer sem.Release(1)
		fetch_puzzle_input(year, day, client)
	}()
}

func fetch_puzzle_input(
	year, day int,
	client *resty.Client,
) {
	prefix := fmt.Sprintf("year=%v day=%v", year, day)
	url := fmt.Sprintf("https://adventofcode.com/%v/day/%v/input", year, day)
	file_path := filepath.Join(INPUTS_DIR, fmt.Sprintf("%v/day%v.txt", year, day))

	if _, err := os.Stat(file_path); !os.IsNotExist(err) {
		print("%v exists: skipping", prefix)
		return
	}

	print("%v fetching...", prefix)
	resp, err := client.R().Get(url)
	if err != nil {
		print("%v %v ERROR: %v", prefix, resp.StatusCode(), err)
	}
	data := resp.Body()

	os.MkdirAll(filepath.Dir(file_path), os.ModePerm)
	file, err := os.Create(file_path)
	if err != nil {
		panic(fmt.Sprintf("Couldn't open file %v: %v", file, err))
	}
	defer file.Close()
	file.Write(data)
	print("%v fetched; saved to %v", prefix, file_path)
}

func load_session_cookie() string {
	path := "../.aoc-session"
	data, err := os.ReadFile(path)
	if err != nil {
		log.Fatal(err)
	}
	return strings.TrimSpace(string(data))
}

func calculate_years_and_days() []Job {
	this_year, this_month, this_day := time.Now().Date()
	fmt.Println(this_year)
	jobs := []Job{}

	// Add jobs for all the past years' puzzles
	for year := FIRST_YEAR; year < this_year; year++ {
		for day := 1; day <= 25; day++ {
			job := Job{year: year, day: day}
			jobs = append(jobs, job)
		}
	}

	// If it is December, we also want to add jobs for all the puzzles that have
	// been released so far.
	if this_month.String() == "December" {
		for day := 1; day <= this_day; day++ {
			job := Job{year: this_year, day: day}
			jobs = append(jobs, job)
		}
	}

	return utils.Reverse(jobs)
}

func print(format string, args ...any) {
	formatted := fmt.Sprintf(format, args...)
	fmt.Println(formatted)
}
