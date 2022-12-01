import * as fs from "fs"
var path = require("path")


export function loadPuzzleInput(filename: string) {
    const p = path.join(__dirname, `../puzzle_inputs/${filename}.txt`)
    return fs.readFileSync(p, "utf8")
}

if (require.main === module) {
    console.log(loadPuzzleInput("2020/day1"))
}