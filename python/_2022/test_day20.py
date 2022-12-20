import pytest
from redbreast.testing import parametrize, testparams

from python._2022.day20 import shift_number, shift_naive


@parametrize(
    param := testparams("before", "item", "move", "expected_result"),
    [
        param(
            before=(1, 2, -3, 3, -2, 0, 4),
            item=1,
            move=1,
            expected_result=(2, 1, -3, 3, -2, 0, 4),
        ),
        param(
            before=(2, 1, -3, 3, -2, 0, 4),
            item=2,
            move=2,
            expected_result=(1, -3, 2, 3, -2, 0, 4),
        ),
        param(
            before=(1, -3, 2, 3, -2, 0, 4),
            item=-3,
            move=-3,
            expected_result=(1, 2, 3, -2, -3, 0, 4),
        ),
        param(
            before=(1, 2, 3, -2, -3, 0, 4),
            item=3,
            move=3,
            expected_result=(1, 2, -2, -3, 0, 3, 4),
        ),
        param(
            before=(1, 2, -2, -3, 0, 3, 4),
            item=-2,
            move=-2,
            expected_result=(1, 2, -3, 0, 3, 4, -2),
        ),
        param(
            before=(1, 2, -3, 0, 3, 4, -2),
            item=0,
            move=0,
            expected_result=(1, 2, -3, 0, 3, 4, -2),
        ),
        param(
            before=(1, 2, -3, 0, 3, 4, -2),
            item=4,
            move=4,
            expected_result=(1, 2, -3, 4, 0, 3, -2),
        ),
        param(
            before=(1, 2, 3, 4),
            item=3,
            move=-3,
            expected_result=(1, 2, 3, 4),
            description="wrap all the way around",
        ),
        param(
            before=(1, 2, 3, 4),
            item=3,
            move=-6,
            expected_result=(1, 2, 3, 4),
            description="wrap all the way around twice",
        ),
        param(
            before=(1, 2, 3, 4),
            item=3,
            move=-4,
            expected_result=(1, 3, 2, 4),
            description="wrap all the way around + 1",
        ),
        param(
            before=(1, 2, 3, 4),
            item=3,
            move=-7,
            expected_result=(1, 3, 2, 4),
            description="wrap all the way around twice + 1",
        ),
        param(
            before=(1, 2, 3, 4),
            item=3,
            move=3,
            expected_result=(1, 2, 3, 4),
            description="wrap all the way around forwards",
        ),
        param(
            before=(1, 2, 3, 4),
            item=3,
            move=4,
            expected_result=(1, 2, 4, 3),
            description="wrap all the way around forwards + 1",
        ),
        param(
            before=(1, 2, 3, 4),
            item=3,
            move=6,
            expected_result=(1, 2, 3, 4),
            description="wrap all the way around forwards twice",
        ),
        param(
            before=(1, 2, 3, 4),
            item=3,
            move=7,
            expected_result=(1, 2, 4, 3),
            description="wrap all the way around forwards twice + 1",
        ),
        param(
            before=(1, 2, 3, 4),
            item=3,
            move=10,
            expected_result=(1, 2, 4, 3),
            description="wrap all the way around forwards 3x + 1",
        ),
        param(
            description="custom",
            before=(1, 2, -3, 3, -2, 0, 4),
            item=2,
            move=-5,
            expected_result=(1, -3, 2, 3, -2, 0, 4),
        ),
    ],
)
@pytest.mark.parametrize("func", [shift_naive, shift_number])
def test_shift_funcs(func, param):
    assert func(
        list(param.before),
        param.item,
        param.move,
        len(param.before),
    ) == list(param.expected_result)
