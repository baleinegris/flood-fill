import React from "react";
import { Gauge, gaugeClasses } from '@mui/x-charts/Gauge';

export default function DangerBar({ percent }) {
    return (
      <Gauge
        value={percent}
        startAngle={0}
        endAngle={360}
        width={100}
        height={100}
        sx={{
          [`& .${gaugeClasses.valueText}`]: {
            fontSize: 15,
            transform: 'translate(0px, 0px)',
          },
          [`& .${gaugeClasses.valueArc}`]: {
            fill: percent > 80 ? 'red' : percent > 50 ? 'orange' : 'green',
          },
        }}
        text={({ value, valueMax }) => `${percent}%`}
      />
    );
  }