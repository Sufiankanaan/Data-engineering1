"""Tests for the data pipeline."""

import pandas as pd
import pytest

from pipeline import transform, extract, parse_month


# ---------- transform() ----------

def test_transform_adds_month_column():
    """The month column should exist after transform."""
    df = pd.DataFrame({"day": [1, 2], "num_passengers": [3, 4]})
    result = transform(df, month=10)
    assert "month" in result.columns


def test_transform_adds_correct_month_value():
    """The month column should hold the value we passed."""
    df = pd.DataFrame({"day": [1, 2], "num_passengers": [3, 4]})
    result = transform(df, month=7)
    assert (result["month"] == 7).all()


def test_transform_does_not_modify_original():
    """transform() should not mutate the input DataFrame."""
    df = pd.DataFrame({"day": [1], "num_passengers": [3]})
    transform(df, month=5)
    assert "month" not in df.columns


# ---------- extract() ----------

def test_extract_returns_expected_columns():
    """extract() should return the expected schema."""
    df = extract()
    assert list(df.columns) == ["day", "num_passengers"]


def test_extract_is_not_empty():
    """extract() should return at least one row."""
    df = extract()
    assert len(df) > 0


# ---------- parse_month() ----------

def test_parse_month_accepts_valid_month():
    """A valid month should be returned as an integer."""
    assert parse_month(["pipeline.py", "10"]) == 10


def test_parse_month_accepts_boundary_months():
    """Months 1 and 12 are valid edge cases."""
    assert parse_month(["pipeline.py", "1"]) == 1
    assert parse_month(["pipeline.py", "12"]) == 12


def test_parse_month_rejects_missing_argument():
    """No month argument should exit the program."""
    with pytest.raises(SystemExit):
        parse_month(["pipeline.py"])


def test_parse_month_rejects_text():
    """A non-numeric month should exit the program."""
    with pytest.raises(SystemExit):
        parse_month(["pipeline.py", "hello"])


def test_parse_month_rejects_month_too_high():
    """Month 13 is out of range and should exit."""
    with pytest.raises(SystemExit):
        parse_month(["pipeline.py", "13"])


def test_parse_month_rejects_month_zero():
    """Month 0 is out of range and should exit."""
    with pytest.raises(SystemExit):
        parse_month(["pipeline.py", "0"])