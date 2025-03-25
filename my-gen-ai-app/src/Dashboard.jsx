import { useContext, useEffect, useState } from "react";
import { AppSidebar } from "@/components/app-sidebar"
import { ChartAreaInteractive } from "@/components/chart-area-interactive"
import { DataTable } from "@/components/data-table"
import { SectionCards } from "@/components/section-cards"
import { SiteHeader } from "@/components/site-header"
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar"
import { MyContext } from "./app-route";
import { getTopRequestTypes } from "./utils/utils";
import { Outlet, useLocation } from "react-router-dom";

export const SideBarCharts = ({ totalCount, topThreeRequests}) => {
  return (
    <SidebarInset>
      <SiteHeader />
        <div className="flex flex-1 flex-col">
          <div className="@container/main flex flex-1 flex-col gap-2">
            <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
              <SectionCards totalCount={totalCount} topThreeRequests={topThreeRequests} />
              <div className="px-4 lg:px-6">
                <ChartAreaInteractive />
              </div>
            </div>
          </div>
        </div>
      </SidebarInset>
  )
}
export default function Dashboard() {
  const { contextData, setContextData } = useContext(MyContext);
  const [totalCount, setTotalCount] = useState(0);
  const [topThreeRequests, setTopThreeRequests] = useState('');
  
  const location = useLocation(); // Get the current location object;
  const locationPathname = location.pathname; // Get the current location pathname;
  const isEmailClassification = locationPathname.includes("email-classifications") || locationPathname.includes("configuration") || locationPathname.includes("create-service-request-demo");
  console.log("Is Email Classification:", isEmailClassification);   
  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8765");

    socket.onopen = () => {
      console.log("Connected to WebSocket server");
      socket.send("Hello from client");
    };

    socket.onmessage = (event) => {
      console.log("Received from server:", JSON.parse(event.data));
      let serverData = JSON.parse(event.data);
      if(serverData?.type === "storage_data"){
        setContextData(serverData);
        console.log("Context Value:", contextData?.payload);
        //const extractOuput = extractClassificationsDetails(contextData?.payload);
        const totalCount = contextData?.payload?.length; //getTotalCount(extractOuput)
        const topThreeRequests = getTopRequestTypes(contextData?.payload);
        console.log('topThreeRequests', topThreeRequests);
        setTotalCount(totalCount);
        setTopThreeRequests(topThreeRequests);
      }
      
    };

    return () => {
      socket.close();
    };
  }, []);
  console.log('topThreeRequests dash', isEmailClassification)
  return (
    <SidebarProvider>
      <AppSidebar variant="inset" />
      {!isEmailClassification && <SideBarCharts totalCount={totalCount} topThreeRequests={topThreeRequests}/>}
      {/* <SidebarInset>
      <SiteHeader />
        <div className="flex flex-1 flex-col">
          <div className="@container/main flex flex-1 flex-col gap-2">
            <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
              <SectionCards totalCount={totalCount} topThreeRequests={topThreeRequests} />
              <div className="px-4 lg:px-6">
                <ChartAreaInteractive />
              </div>
            </div>
          </div>
        </div>
      </SidebarInset> */}
      <Outlet />
    </SidebarProvider>
  )
}
