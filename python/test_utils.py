from redbreast.testing import parametrize, testparams

from python.utils import SparseMatrix, sparse_matrix_string


@parametrize(
    param := testparams("grid", "flip_y", "pad", "empty_char", "expected"),
    [
        param(
            description="Empty default behaviour",
            grid=SparseMatrix(),
            flip_y=False,
            pad=0,
            empty_char=".",
            expected=".",
        ),
        param(
            description="Empty with flip",
            grid=SparseMatrix(),
            flip_y=True,
            pad=0,
            empty_char=".",
            expected=".",
        ),
        param(
            description="Empty with pad",
            grid=SparseMatrix(),
            flip_y=False,
            pad=1,
            empty_char=".",
            expected="\n".join(
                [
                    "...",
                    "...",
                    "...",
                ]
            ),
        ),
        param(
            description="Empty with pad and flip",
            grid=SparseMatrix(),
            flip_y=True,
            pad=1,
            empty_char=".",
            expected="\n".join(
                [
                    "...",
                    "...",
                    "...",
                ]
            ),
        ),
        param(
            description="Single entry default behaviour",
            grid=SparseMatrix({(0, 0): "A"}),
            flip_y=False,
            pad=0,
            empty_char=".",
            expected="A",
        ),
        param(
            description="Single entry with flip",
            grid=SparseMatrix({(0, 0): "A"}),
            flip_y=True,
            pad=0,
            empty_char=".",
            expected="A",
        ),
        param(
            description="Single entry with pad",
            grid=SparseMatrix({(0, 0): "A"}),
            flip_y=False,
            pad=1,
            empty_char=".",
            expected="\n".join(
                [
                    "...",
                    ".A.",
                    "...",
                ]
            ),
        ),
        param(
            description="Single entry with pad and flip",
            grid=SparseMatrix({(0, 0): "A"}),
            flip_y=True,
            pad=1,
            empty_char=".",
            expected="\n".join(
                [
                    "...",
                    ".A.",
                    "...",
                ]
            ),
        ),
        param(
            description="Non-empty default behaviour",
            grid=SparseMatrix(
                {
                    (0, 0): "A",
                    (2, 3): "B",
                }
            ),
            flip_y=False,
            pad=0,
            empty_char=".",
            expected="\n".join(
                [
                    "A..",
                    "...",
                    "...",
                    "..B",
                ]
            ),
        ),
        param(
            description="Non-empty with flip",
            grid=SparseMatrix(
                {
                    (0, 0): "A",
                    (2, 3): "B",
                }
            ),
            flip_y=True,
            pad=0,
            empty_char=".",
            expected="\n".join(
                [
                    "..B",
                    "...",
                    "...",
                    "A..",
                ]
            ),
        ),
        param(
            description="Non-empty with pad",
            grid=SparseMatrix(
                {
                    (0, 0): "A",
                    (2, 3): "B",
                }
            ),
            flip_y=False,
            pad=2,
            empty_char=".",
            expected="\n".join(
                [
                    ".......",
                    ".......",
                    "..A....",
                    ".......",
                    ".......",
                    "....B..",
                    ".......",
                    ".......",
                ]
            ),
        ),
        param(
            description="Non-empty with pad and flip",
            grid=SparseMatrix(
                {
                    (0, 0): "A",
                    (2, 3): "B",
                }
            ),
            flip_y=True,
            pad=2,
            empty_char=".",
            expected="\n".join(
                [
                    ".......",
                    ".......",
                    "....B..",
                    ".......",
                    ".......",
                    "..A....",
                    ".......",
                    ".......",
                ]
            ),
        ),
    ],
)
def test_sparse_matrix_string(param):
    result = sparse_matrix_string(
        grid=param.grid,
        flip_y=param.flip_y,
        pad=param.pad,
        empty_char=param.empty_char,
    )
    assert result == param.expected
