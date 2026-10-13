from agent import sum_budget, days_between, lookup_topic, manage_history
from langchain_core.messages import HumanMessage, AIMessage
import pytest


def test_money_precision_and_validation():
    assert sum_budget.invoke({"amounts": [0.1, 0.2]}) == "0.30"
    assert sum_budget.invoke({"amounts": [12.5, 8, 20]}) == "40.50"
    with pytest.raises(ValueError):
        sum_budget.invoke({"amounts": [-1]})


def test_dates():
    assert days_between.invoke({"start_date": "2026-10-10", "end_date": "2026-10-13"}) == 3
    assert days_between.invoke({"start_date": "2026-10-13", "end_date": "2026-10-13"}) == 0


def test_lookup_unknown():
    assert "Volume" in lookup_topic.invoke({"topic": "Docker"})
    assert "没有" in lookup_topic.invoke({"topic": "Redis"})
