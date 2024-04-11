import React from "react";
import Sidebar from "./Sidebar";

const Dashboard = () => {
  return (
    <>
      <div className="flex">
        <Sidebar />
        <div className="flex xl:flex-col w-full h-screen overflow-auto">
          <div className="w-[50%] h-screen xl:w-[100%] xl:min-h-[78vh]">
            <iframe
              title="line-chart"
              src="https://sample.kmdo.app/widgets/reports/line-chart"
              style={{ width: "100%", height: "100%", border: "none" }}
              allowFullScreen
            />
          </div>
          <div className="w-[50%] h-screen xl:w-[100%] xl:min-h-[78vh]">
            <iframe
              title="line-chart"
              src="https://sample.kmdo.app/widgets/reports/pie-chart"
              style={{ width: "100%", height: "100%", border: "none" }}
              allowFullScreen
            />
          </div>
        </div>
      </div>
    </>
  );
};

export default Dashboard;
