import React from "react";
import Sidebar from "./Sidebar";

const ChartDashboard = () => {
  return (
    <div className="flex">
      <Sidebar />
      <div className="flex" style={{ width: "100%", height: "100vh" }}>
        <iframe
          title="line-chart"
          src="https://sample.kmdo.app/widgets/reports/pie-chart"
          style={{ width: "100%", height: "100%", border: "none" }}
          allowFullScreen
        />
      </div>
    </div>
  );
};

export default ChartDashboard;
