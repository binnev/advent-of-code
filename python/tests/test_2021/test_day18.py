import pytest
from puzzles.y2021.day18 import explode, split, add, magnitude


@pytest.mark.parametrize(
    "string, expected",
    [
        ("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"),
        ("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"),
        ("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"),
        ("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"),
        ("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"),
        ("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]", "[[[[0,7],4],[7,[[8,4],9]]],[1,1]]"),
        ("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]", "[[[[0,7],4],[15,[0,13]]],[1,1]]"),
    ],
)
def test_explode(string, expected):
    result, changed = explode(string)
    assert result == expected


@pytest.mark.parametrize(
    "string, expected",
    [
        ("[[[[0,7],4],[15,[0,13]]],[1,1]]", "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"),
        ("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]", "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"),
    ],
)
def test_split(string, expected):
    result, changed = split(string)
    assert result == expected


@pytest.mark.parametrize(
    "left, right, expected",
    [
        ("[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]", "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"),
        (
            "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
            "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
            "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]",
        ),
    ],
)
def test_add(left, right, expected):
    result = add(left, right)
    assert result == expected


@pytest.mark.parametrize(
    "string, expected",
    [
        ("[[1,2],[[3,4],5]]", 143),
        ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
        ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
        ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
        ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
        ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488),
    ],
)
def test_magnitude(string, expected):
    result = magnitude(string)
    assert result == expected
