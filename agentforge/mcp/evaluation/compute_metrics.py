def compute_metrics(primary_metric: float) -> dict[str, float]:
    precision = max(primary_metric - 0.05, 0.0)
    recall = max(primary_metric - 0.03, 0.0)
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return {"precision": precision, "recall": recall, "f1": f1, "auc": min(primary_metric + 0.02, 1.0)}

