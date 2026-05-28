from __future__ import annotations

import api  # noqa: F401 — triggers sys.path setup in api/__init__.py

from huskyadvisor.advisor import HuskyAdvisorEngine
from huskyadvisor.service import build_json_advisor

_engine: HuskyAdvisorEngine | None = None


def get_engine() -> HuskyAdvisorEngine:
    global _engine
    if _engine is None:
        _engine = build_json_advisor()
    return _engine
