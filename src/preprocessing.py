import pandas as pd
import numpy as np
from typing import Tuple


def remove_noise(df: pd.DataFrame, z_thresh: float = 3.5) -> pd.DataFrame:
    """Remove extreme spikes using z-score clipping per numeric column."""
    numeric = df.select_dtypes(include=[np.number])
    z = (numeric - numeric.mean()) / numeric.std(ddof=0)
    mask = (z.abs() <= z_thresh).all(axis=1)
    return df.loc[mask].reset_index(drop=True)


def handle_missing_values(df: pd.DataFrame, strategy: str = "mean") -> pd.DataFrame:
    """Fill or drop missing values. strategy: 'mean'|'median'|'drop'"""
    if strategy == "drop":
        return df.dropna().reset_index(drop=True)
    numeric = df.select_dtypes(include=[np.number])
    if strategy == "mean":
        filled = numeric.fillna(numeric.mean())
    else:
        filled = numeric.fillna(numeric.median())
    non_numeric = df.select_dtypes(exclude=[np.number])
    return pd.concat([non_numeric.reset_index(drop=True), filled.reset_index(drop=True)], axis=1)


def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    """Scale numeric columns to [0,1] per-column (min-max)."""
    numeric = df.select_dtypes(include=[np.number]).copy()
    denom = numeric.max() - numeric.min()
    denom = denom.replace(0, 1)
    numeric = (numeric - numeric.min()) / denom
    others = df.select_dtypes(exclude=[np.number]).reset_index(drop=True)
    return pd.concat([others, numeric.reset_index(drop=True)], axis=1)


def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    """Derive simple rolling features per equipment (if timestamp present, assumes ordered data).

    Produces mean, std, rms, and kurtosis for numeric columns.
    """
    from scipy.stats import kurtosis

    numeric = df.select_dtypes(include=[np.number])
    features = {}
    for col in numeric.columns:
        arr = numeric[col].values
        features[f"{col}_mean"] = np.nanmean(arr)
        features[f"{col}_std"] = np.nanstd(arr)
        features[f"{col}_rms"] = np.sqrt(np.nanmean(arr ** 2))
        try:
            features[f"{col}_kurtosis"] = float(kurtosis(arr, nan_policy="omit"))
        except Exception:
            features[f"{col}_kurtosis"] = 0.0

    return pd.DataFrame([features])


def split_data(df: pd.DataFrame, target_col: str, train_size: float = 0.8):
    """Split into X_train, X_test, y_train, y_test by simple index split."""
    n = len(df)
    cutoff = int(n * train_size)
    X = df.drop(columns=[target_col])
    y = df[target_col]
    return X.iloc[:cutoff], X.iloc[cutoff:], y.iloc[:cutoff], y.iloc[cutoff:]
