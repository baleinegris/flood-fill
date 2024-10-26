import React from "react";
import DangerBar from "./DangerBar";

export default function ReportSection({ precipitation, danger} ) {
    return (
        <div className="flex items-center h-[40%]">
        <div className="flex flex-col">
            <div className="text-black"> Average Precipitation: {precipitation}mm</div>
            <div className="text-black"> Canadian Average: CONST</div>
            <div className="text-black"> Danger Level: {danger}</div>
        </div>
        <DangerBar percent={80} />
    </div>
    )
};