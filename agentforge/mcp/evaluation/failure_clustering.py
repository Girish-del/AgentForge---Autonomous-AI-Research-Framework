def failure_clustering(primary_metric: float) -> dict[str, str]:
    if primary_metric < 0.7:
        cluster = "data_distribution_shift"
    elif primary_metric < 0.85:
        cluster = "model_capacity_limit"
    else:
        cluster = "rare_edge_cases"
    return {"top_failure_mode": cluster, "method": "umap_kmeans_stub"}

