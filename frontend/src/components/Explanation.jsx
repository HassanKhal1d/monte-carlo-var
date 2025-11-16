import React from "react";

export default function Explanation({metrics}){
  const {risk, stats, n_sims, horizon_days} = metrics;
  const text = `Horizon: ${horizon_days} day(s). Simulations: ${n_sims}.
95% VaR = ${(risk.VaR*100).toFixed(2)}% ; 95% CVaR = ${(risk.CVaR*100).toFixed(2)}%.
Mean return ${(stats.mean*100).toFixed(3)}%, Std ${(stats.std*100).toFixed(3)}%.`;
  return (
    <div style={{marginTop:10}}>
      <h3>Risk Summary</h3>
      <pre>{text}</pre>
    </div>
  );
}

