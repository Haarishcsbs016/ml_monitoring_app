import pandas as pd
from src.preprocessing import normalize_data, handle_missing_values


def test_handle_missing():
    df = pd.DataFrame({"a": [1, None, 3], "b": [4, 5, None]})
    out = handle_missing_values(df, strategy="mean")
    assert not out["a"].isna().any()
    assert not out["b"].isna().any()


def test_normalize():
    df = pd.DataFrame({"a": [0, 5, 10], "b": [1, 1, 1]})
    out = normalize_data(df)
    assert out["a"].max() <= 1.0
    assert out["a"].min() >= 0.0
