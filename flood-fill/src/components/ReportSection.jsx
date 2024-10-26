import React from "react";
import DangerBar from "./DangerBar";
import histogram from './mock_histogram.png';
export default function ReportSection({ precipitation, expectedFloods, graph } ) {
    return (
        <div className="flex items-start h-[40%] justify-start">
        <div className="flex flex-col w-[60%]">
            <div className="text-black"> Average Precipitation: {precipitation}mm</div>
            <div className="text-black"> Canadian Average: CONST</div>
            <div className="text-black"> Expected number of floods per year:</div>
            <div className="flex flex-col items-align justify-center">
            Projected number of floods:
            <img src={histogram} className=""/>
            </div>

</div>
        <div className="flex flex-col w-[40%]">
            <div className="text-black font-bold"> Danger Level:</div>
            <DangerBar percent={80} />
        </div>
    </div>
    )
};