"use client"

import { useContext, useEffect, useState } from "react";
import {
  AudioWaveform,
  BookOpen,
  Bot,
  Command,
  Frame,
  GalleryVerticalEnd,
  Map,
  PieChart,
  Settings2,
  SquareTerminal,
} from "lucide-react"

import { NavMain } from "@/components/nav-main"
import { NavProjects } from "@/components/nav-projects"
import { NavUser } from "@/components/nav-user"
import { TeamSwitcher } from "@/components/team-switcher"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from "@/components/ui/sidebar"
import { MyContext } from "../app-route";
import { extractClassificationsDetails } from "../utils/utils";

// import data from "./data.json"

// This is sample data.

let data = {
  user: {
    name: "XYZ",
    email: "xyz@example.com",
    avatar: "",
  },
  teams: [
    {
      name: "Loan Servicing Platform",
      logo: GalleryVerticalEnd,
      plan: "Service Requests",
    },
    {
      name: "Acme Corp.",
      logo: AudioWaveform,
      plan: "Startup",
    },
    {
      name: "Evil Corp.",
      logo: Command,
      plan: "Free",
    }
  ],
  navMain: [],
  projects: [
    {
      name: "Design Engineering",
      url: "#",
      icon: Frame,
    },
    {
      name: "Sales & Marketing",
      url: "#",
      icon: PieChart,
    },
    {
      name: "Travel",
      url: "#",
      icon: Map,
    },
  ],
}

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const { contextData } = useContext(MyContext);
  const [classificationDetails, setClassificationDetails] = useState(contextData?.payload)
  
  useEffect(() => {
    const extractOuput = extractClassificationsDetails(contextData?.payload);
    setClassificationDetails(extractOuput);
    classificationDetails && Object.keys(classificationDetails).map((item) => {
      if((item !== '0' && item !== '1')){
        return  data.navMain.push({
          title: item,
          url: "#/",
          icon: SquareTerminal,
          isActive: true,
          items: classificationDetails[item].map((subItem) => {
            return {
              title: subItem,
              url: "#/",
              isActive: true,
            }
          })
    })
      }
    })
  }, [contextData])
  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <TeamSwitcher teams={data.teams} />
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={data.navMain} />
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={data.user} />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}
