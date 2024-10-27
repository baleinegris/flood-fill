import React from "react";
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import ReportSection from "./ReportSection";
import Box from '@mui/material/Box';

function CustomTabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

function a11yProps(index) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

export default function Report({ name, data }) {
  const [value, setValue] = React.useState(0);
  const presentPrecip = data.expected_floods['2024'][1];
  const presentFloods = data.expected_floods['2024'][0];
  const presentDanger = (1 - Math.exp(-presentFloods));
  const futurePrecip = data.expected_floods['2030'][1];
  const futureFloods = data.expected_floods['2030'][0];
  const futureDanger = (1 - Math.exp(-futureFloods));
  const imgHref = data.plot

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <div className="flex flex-col items-center border-black border-2 bg-white rounded-lg max-w-[90%]"> 
        <div className=" m-6 text-lg font-bold">
            Flood Report for {name}
        </div>
        <div className="w-full h-[1px] bg-black" />
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={value} onChange={handleChange} aria-label="basic tabs example">
            <Tab label="Present" {...a11yProps(0)} />
            <Tab label="Future (Predicted)" {...a11yProps(1)} />
            </Tabs>
        </Box>
        <CustomTabPanel value={value} index={0}>
            <ReportSection graphHref={imgHref} expectedFloods={presentFloods} precipitation={presentPrecip} danger={presentDanger}/>
        </CustomTabPanel>
        <CustomTabPanel value={value} index={1}>
        <ReportSection graphHref={imgHref} expectedFloods={futureFloods} precipitation={futurePrecip} danger={futureDanger}/>
        </CustomTabPanel>
    </div>
  );
}


// export default function Report({ name, precipitation, danger }){
//     return (
//         <div className="flex flex-col items-center w-[1000px] h-[500px] border-black border-2">
//             <div className=" m-6">
//                 Report for {name}
//             </div>
//             <Tabs>
//                 <Tab label="Present" value={1}/>
//                 <Tab label="Future" />
//             </Tabs>
//             <TabPanel value={1}> 
//                 <ReportSection precipitation={precipitation} danger={danger}/>
//             </TabPanel>
//         </div>
//     )
// }