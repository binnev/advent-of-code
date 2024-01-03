import pytest

from puzzles.y2023.day17 import *

example = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

small3 = """
111
222
333"""
small3_solution = """
111
..2
..3"""

small4 = """
1111
2222
3333
4444"""
small4_solution = """
1111
...2
...3
...4
"""

small5 = """
11111
22222
33333
44444
55555"""
small5_solution = """
1111.
...22
....3
....4
....5"""

small6 = """
111111
222222
333333
444444
555555
666666
"""
small6_solution = """
1111..
...22.
....33
.....4
.....5
.....6
"""

small4_diagonal = """
1555
1155
5115
5511
"""
small4_diagonal_solution = """
1...
11..
.11.
..11
"""

small6_nonlinear = """
188111
111181
888881
888111
888188
888111
"""
small6_nonlinear_solution = """
1..111
1111.1
.....1
...111
...1..
...111
"""

small6_diagonal = """
155555
115555
511555
551155
555115
555511
"""
small6_diagonal_solution = """
1.....
11....
.11...
..11..
...11.
....11
"""


@pytest.mark.parametrize(
    "input, expected_length, expected_path",
    [
        # (small3, 7, small3_solution),
        # (small4, 12, small4_solution),
        # (small5, 19, small5_solution),
        (small6, 28, small6_solution),
        (small4_diagonal, 6, small4_diagonal_solution),
        (small6_diagonal, 10, small6_diagonal_solution),
        (small6_nonlinear, 16, small6_nonlinear_solution),
        (example, 102, "example_solution"),
    ],
)
def test_dijkstra(input, expected_length, expected_path):
    matrix = parse_input(input)
    _, xmax = matrix.get_xlim()
    _, ymax = matrix.get_ylim()
    start = (0, 0)
    finish = (xmax, ymax)
    distances, prev_nodes = dijkstra(start, finish, matrix)

    print("")
    print("=" * 20)
    print("for matrix:")
    matrix.print()
    print("-" * 20)
    print("I found the best path:")
    best_path_nodes = get_best_path(prev_nodes, finish)
    best_path_matrix = SparseMatrix({node: matrix[node] for node in best_path_nodes})
    best_path_matrix.print()

    assert distances[finish] == expected_length
    assert best_path_matrix.to_str().strip() == expected_path.strip()
