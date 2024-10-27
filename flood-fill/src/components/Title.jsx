import React from "react";
import logo from '/logo - Copy.png';

export default function Title(){
    return (
        <div className="flex justify-center items-center relative bg-[#0a1627] translate-y-[-10px]">
            {/* <div className="bg-gradient-to-r from-cyan-500 to-blue-500 to-pink-500 font-bold m-6 text-[3em] bg-clip-text text-transparent">
                FLOOD FILL
            </div> */}
            <img src={logo} style = {{height: '100px', borderRadius: '50px'}}/>
        </div>
    )
}