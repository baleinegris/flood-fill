import React, { createContext, useState } from 'react';

export const ReportContext = createContext();

export const ReportProvider = ({ children }) => {
  const [reportView, setReportView] = useState(false);
  const [activeReport, setActiveReport] = useState(0);

  return (
    <ReportContext.Provider value={{ reportView, setReportView, activeReport, setActiveReport }}>
      {children}
    </ReportContext.Provider>
  );
};

export default ReportProvider;