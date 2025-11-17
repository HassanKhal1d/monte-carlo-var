import React, { useState } from "react";
import Controls from "./components/Controls";
import Chart from "./components/Chart";
import Explanation from "./components/Explanation";

export default function App(){
  const [paths, setPaths] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(false);

  async function runSim(inputs){
    setLoading(true);
    const body = {
      s0: inputs.s0 || null,
      horizon_days: inputs.horizon,
      n_sims: inputs.nSims,
      jump_lambda: inputs.jumpLambda,
      jump_mu: inputs.jumpMu,
      jump_sigma: inputs.jumpSigma,
      seed: inputs.seed || null,
      use_jump: inputs.useJump
    };
    try{
      const res = await fetch("http://localhost:8000/simulate", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(body)
      });
      const data = await res.json();
      setPaths(data.paths);
      setMetrics(data);
    }catch(e){
      alert("Error contacting backend. Ensure FastAPI is running on port 8000.");
    }
    setLoading(false);
  }

  return (
    <div style={{padding:20, fontFamily:"Arial, sans-serif"}}>
      <h1>Monte Carlo VaR Model</h1>
      <Controls onRun={runSim} loading={loading}/>
      {metrics && <Explanation metrics={metrics} />}
      {paths.length>0 && <Chart paths={paths} />}
    </div>
  )
}

