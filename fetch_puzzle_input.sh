set -e  # fail on errors
DIR=".puzzle-inputs/$1"
curl -O https://adventofcode.com/$1/day/$2/input \
    --header "Cookie: session=$(cat .aoc-session)" \
    --fail
mkdir -p $DIR
mv input $DIR/day$2.txt
