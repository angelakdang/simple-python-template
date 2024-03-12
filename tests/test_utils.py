from datetime import datetime, timedelta

import numpy as np
import polars as pl
import pytest

from src.utils import (
    add_two_numbers,
    check_for_required_columns,
    standardize_date_time_columns,
)


@pytest.mark.parametrize("n1, n2, expected", [(1, 2, 3), (1.0, 4, 5.0), (6.2, 7.1, 13.3)])
def test_add_two_numbers(n1, n2, expected):
    assert add_two_numbers(n1, n2) == expected


def test_check_for_required_columns():
    df = pl.DataFrame(
        {
            "foo": np.random.randint(0, 100, size=5),
            "bar": np.random.randint(0, 100, size=5),
            "cat": np.random.randint(0, 100, size=5),
        }
    )

    check_for_required_columns(df=df, required_columns={"foo", "bar", "cat"})
    pass


def test_check_for_required_columns_error():
    df = pl.DataFrame(
        {
            "foo": np.random.randint(0, 100, size=5),
            "bar": np.random.randint(0, 100, size=5),
            "cat": np.random.randint(0, 100, size=5),
        }
    )

    with pytest.raises(ValueError):
        check_for_required_columns(df=df, required_columns={"foo", "bar", "dog"})


def test_standardize_date_time_columns():
    df = pl.DataFrame(
        {
            "date": [datetime.now() - timedelta(days=i) for i in range(5)],
            "floats": np.random.rand(5),
        }
    )

    output = standardize_date_time_columns(df=df)

    assert output["date"].dtype == pl.Datetime(time_zone=None, time_unit="us")
    assert output["floats"].dtype == pl.Float64


def test_standardize_date_time_columns_to_string():
    df = pl.DataFrame(
        {
            "date": [datetime.now() - timedelta(days=i) for i in range(5)],
            "floats": np.random.rand(5),
        }
    )

    output = standardize_date_time_columns(df=df, to_string=True)

    assert output["date"].dtype == pl.Utf8
    assert output["floats"].dtype == pl.Float64


def test_standardize_date_time_columns_ms():
    df = pl.DataFrame(
        {
            "date": [datetime.now() - timedelta(days=i) for i in range(5)],
            "floats": np.random.rand(5),
        }
    )

    output = standardize_date_time_columns(df=df, time_unit="ms")

    assert output["date"].dtype == pl.Datetime(time_zone=None, time_unit="ms")
    assert output["floats"].dtype == pl.Float64
