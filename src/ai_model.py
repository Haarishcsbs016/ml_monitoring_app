import os
from typing import Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_fscore_support, accuracy_score


def train_model(X: pd.DataFrame, y: pd.Series, n_estimators: int = 100) -> Tuple[RandomForestClassifier, dict]:
    model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
    model.fit(X, y)
    metrics = evaluate_model(model, X, y)
    return model, metrics


def predict_fault(model: RandomForestClassifier, X: pd.DataFrame) -> list:
    probs = model.predict_proba(X)
    classes = model.classes_
    results = []
    for p in probs:
        idx = p.argmax()
        results.append({"class": classes[idx], "confidence": float(p[idx])})
    return results


def evaluate_model(model: RandomForestClassifier, X: pd.DataFrame, y: pd.Series) -> dict:
    preds = model.predict(X)
    acc = accuracy_score(y, preds)
    pr, rc, f1, _ = precision_recall_fscore_support(y, preds, average="weighted", zero_division=0)
    return {"accuracy": float(acc), "precision": float(pr), "recall": float(rc), "f1": float(f1)}


def save_model(model, path: str = "model.joblib") -> None:
    joblib.dump(model, path)


def load_model(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    return joblib.load(path)
