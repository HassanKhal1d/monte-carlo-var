import React, {useEffect, useRef} from "react";
import ChartJS from "chart.js/auto";

export default function Chart({paths}){
  const canvasRef = useRef(null);
  useEffect(()=>{
    const ctx = canvasRef.current.getContext("2d");
    const datasets = paths.slice(0, Math.min(100, paths.length)).map((p,i)=>({
      label:`sim-${i}`,
      data: p.map((v,idx)=>({x: idx, y: v})),
      borderWidth: 1,
      pointRadius: 0,
      tension: 0.1
    }));
    const chart = new ChartJS(ctx, {
      type: "line",
      data: {datasets},
      options: {plugins:{legend:{display:false}}, scales:{x:{title:{display:true,text:"Step"}}, y:{title:{display:true,text:"Index"}}}}
    });
    return ()=> chart.destroy();
  }, [paths]);
  return <canvas ref={canvasRef} height={300}></canvas>;
}

