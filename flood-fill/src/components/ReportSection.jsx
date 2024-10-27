import React from "react";
import DangerBar from "./DangerBar";
import histogram from './mock_histogram.png';
import { styled } from "@mui/material";
export default function ReportSection({ precipitation, expectedFloods, graphHref, danger} ) {
    console.log(graphHref);
    return (
        <div className="flex items-start h-[40%] justify-start">
        <div className="flex flex-col w-[60%]">
            <div className="text-black"> Average Precipitation: {precipitation}mm</div>
            <div className="text-black"> Canadian Average: 537.07mm</div>
            <div className="text-black"> Expected number of floods per year: {expectedFloods}</div>
            <div className="flex flex-col items-align justify-center">
            Projected number of floods:
            <img src={`data:image/jpeg;base64,${graphHref}`} style={{width: "150%"}} className=""/>
            </div>

</div>
        <div className="flex flex-col w-[40%]">
            <div className="text-black font-bold"> Danger Level:</div>
            <DangerBar percent={danger} />
        </div>
    </div>
    )
};