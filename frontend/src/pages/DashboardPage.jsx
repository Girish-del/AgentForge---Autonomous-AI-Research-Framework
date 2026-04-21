import { useState } from "react";

import Spinner from "../components/Spinner";
import apiClient from "../services/apiClient";

function DashboardPage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const runResearch = async () => {
    setLoading(true);
    const response = await apiClient.post("/orchestrator/run", {
      statement: "Improve pick and place success rate by 20%",
      budget_usd: 100,
      max_iterations: 3,
      target_metric: 0.8,
      task_type: "image_classification",
    });
    setResult(response.data);
    setLoading(false);
  };

  return (
    <div>
      <h2>Dashboard</h2>
      <button onClick={runResearch}>Run Experiment</button>
      {loading && <Spinner />}
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
}

export default DashboardPage;
