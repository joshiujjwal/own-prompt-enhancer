"""Smoke tests — verify the package imports without error."""

import src.enhancer.strategies  # noqa: F401
import src.enhancer.orchestrator  # noqa: F401
import src.api.main  # noqa: F401


def test_smoke_import() -> None:
    """Package top-level imports succeed."""
    assert True
