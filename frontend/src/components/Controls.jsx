import React, {useState} from "react";

export default function Controls({onRun, loading}){
  const [s0, setS0] = useState("");
  const [horizon, setHorizon] = useState(1);
  const [nSims, setNSims] = useState(20000);
  const [jumpLambda, setJumpLambda] = useState(0.02);
  const [jumpMu, setJumpMu] = useState(-0.02);
  const [jumpSigma, setJumpSigma] = useState(0.05);
  const [seed, setSeed] = useState("");
  const [useJump, setUseJump] = useState(true);

  return (
    <div style={{marginBottom:20, display:"grid", gridTemplateColumns:"repeat(4, 1fr)", gap:10}}>
      <label>Spot (leave blank to use last historical):<input value={s0} onChange={e=>setS0(e.target.value)} /></label>
      <label>Horizon (days):<select value={horizon} onChange={e=>setHorizon(e.target.value)}>{[...Array(10)].map((_,i)=><option key={i} value={i+1}>{i+1}</option>)}</select></label>
      <label>Simulations:<input type="number" value={nSims} onChange={e=>setNSims(e.target.value)} /></label>
      <label>Seed (optional):<input value={seed} onChange={e=>setSeed(e.target.value)} /></label>

      <label>Jump λ:<input value={jumpLambda} onChange={e=>setJumpLambda(e.target.value)} /></label>
      <label>Jump μ:<input value={jumpMu} onChange={e=>setJumpMu(e.target.value)} /></label>
      <label>Jump σ:<input value={jumpSigma} onChange={e=>setJumpSigma(e.target.value)} /></label>
      <label>Use Jump Diffusion:<input type="checkbox" checked={useJump} onChange={e=>setUseJump(e.target.checked)} /></label>

      <div style={{gridColumn:"1 / -1"}}>
        <button onClick={()=>onRun({s0: s0? parseFloat(s0): null, horizon: parseInt(horizon), nSims: parseInt(nSims), jumpLambda: parseFloat(jumpLambda), jumpMu: parseFloat(jumpMu), jumpSigma: parseFloat(jumpSigma), seed: seed? parseInt(seed): null, useJump})} disabled={loading}>
          {loading? "Running..." : "Simulate"}
        </button>
      </div>
    </div>
  )
}

