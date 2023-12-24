import * as fs from "fs"

var path = require("path")
const { performance } = require("perf_hooks")


export function loadPuzzleInput(filename: string): string {
    const p = path.join(__dirname, `../.puzzle-inputs/${filename}.txt`)
    return fs.readFileSync(p, "utf8").trim()
}

export function profile(func: () => any) {
    const t1 = performance.now()
    const result = func()
    const t2 = performance.now()
    let duration = (t2 - t1) / 1000
    console.log(`${func.name}: ${result} (${duration.toFixed(5)} seconds)`)
    return result
}


if (require.main === module) {
    console.log(loadPuzzleInput("2020/day1"))
}