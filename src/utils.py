"""Utility functions (not service specific)"""

from typing import Literal

import polars as pl
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient


def add_two_numbers(n1: int | float, n2: int | float) -> int | float:
    return n1 + n2


def check_for_required_columns(df: pl.DataFrame, required_columns: set) -> None:
    if not required_columns.issubset(set(df.columns)):
        missing_columns = required_columns.difference(set(df.columns))
        raise ValueError(f"Required columns not present: {missing_columns}")


def standardize_date_time_columns(
    df: pl.DataFrame,
    time_unit: Literal["ns", "us", "ms"] = "us",
    time_zone: str = None,
    to_string: bool = False,
    str_format: str = "%Y/%m/%d %H:%M:%S",
) -> pl.DataFrame:
    """Selects all the temporal (date, datetime, time) columns in a Polars dataframe
    and casts them all to a common time unit and time zone. Option to turn temporal columns into strings.

    :param df: Polars dataframe
    :param time_unit: Literal["ns", "us", "ms"]
        Default is "us"
    :param time_zone: str
        See docs: https://pola-rs.github.io/polars-book/user-guide/transformations/time-series/timezones/
    :param to_string: bool
        Whether to convert datetime columns into string columns
    :param str_format: str
        Format into which to convert the datetime columns

    :return: a Polars dataframe
    """
    temporal_cols = [col for col in df.columns if df[col].is_temporal()]
    df = df.with_columns(pl.col(temporal_cols).dt.cast_time_unit(time_unit).dt.replace_time_zone(time_zone))

    if to_string:
        df = df.with_columns(pl.col(temporal_cols).dt.to_string(format=str_format))

    return df


def retrieve_from_key_vault(
    key_vault_name: str,
    tenant_id: str,
    client_id: str,
    client_secret: str,
    secret_name: str,
) -> str:
    kv_uri = f"https://{key_vault_name}.vault.azure.net"

    credential = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)
    client = SecretClient(vault_url=kv_uri, credential=credential)

    retrieved_secret = client.get_secret(secret_name)

    return retrieved_secret.value
