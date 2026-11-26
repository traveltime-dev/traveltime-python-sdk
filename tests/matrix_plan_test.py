import json
from pathlib import Path

import pytest

from traveltimepy.matrix.plan import Direction, max_batch_size, plan_searches

CASES = json.loads(
    (Path(__file__).parent / "fixtures" / "matrix_plans.json").read_text()
)


@pytest.mark.parametrize("case", CASES, ids=[case["name"] for case in CASES])
def test_plan_matches_fixture(case):
    direction = Direction(case["direction"]) if case["direction"] else None

    plan = plan_searches(
        case["origins"], case["destinations"], case["max_points"], direction
    )

    assert plan.direction.value == case["expected"]["direction"]
    assert [search.id for search in plan.searches] == case["expected"]["searches"]
    batch_size = max_batch_size(
        plan.searches, case["max_searches_per_request"], case["max_points_per_request"]
    )
    assert batch_size == case["expected"]["batch_size"]
