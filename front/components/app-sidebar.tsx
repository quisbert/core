"use client"

import * as React from "react"

import { useAppStore } from "@/stores/app.store"
import { useAuthStore } from "@/stores/auth.store"

import { NavMain } from "@/components/nav-main"
import { NavSecondary } from "@/components/nav-secondary"
import { NavUser } from "@/components/nav-user"

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"

import {
  LayoutDashboardIcon,
  ListIcon,
  ChartBarIcon,
  FolderIcon,
  UsersIcon,
  Settings2Icon,
  CircleHelpIcon,
  SearchIcon,
  CommandIcon,
} from "lucide-react"

const data = {
  navMain: [
    {
      title: "Dashboard",
      url: "#",
      icon: <LayoutDashboardIcon />,
    },
    {
      title: "Lifecycle",
      url: "#",
      icon: <ListIcon />,
    },
    {
      title: "Analytics",
      url: "#",
      icon: <ChartBarIcon />,
    },
    {
      title: "Projects",
      url: "#",
      icon: <FolderIcon />,
    },
    {
      title: "Team",
      url: "#",
      icon: <UsersIcon />,
    },
  ],

  navSecondary: [
    {
      title: "Settings",
      url: "#",
      icon: <Settings2Icon />,
    },
    {
      title: "Get Help",
      url: "#",
      icon: <CircleHelpIcon />,
    },
    {
      title: "Search",
      url: "#",
      icon: <SearchIcon />,
    },
  ],
}

export function AppSidebar(
  props: React.ComponentProps<typeof Sidebar>,
) {

  const { organization } = useAppStore()

  const { user } = useAuthStore()

  return (

    <Sidebar collapsible="offcanvas" {...props}>

      <SidebarHeader>

        <SidebarMenu>

          <SidebarMenuItem>

            <SidebarMenuButton
              render={<a href="#" />}
              className="data-[slot=sidebar-menu-button]:p-1.5!"
            >

              <CommandIcon className="size-5!" />

              <span className="text-base font-semibold">
                {
                  organization?.system_name ??
                  "Core API"
                }
              </span>

            </SidebarMenuButton>

          </SidebarMenuItem>

        </SidebarMenu>

      </SidebarHeader>

      <SidebarContent>

        <NavMain items={data.navMain} />

        <NavSecondary
          items={data.navSecondary}
          className="mt-auto"
        />

      </SidebarContent>

      <SidebarFooter>

        <NavUser
          user={{
            name:
              user?.full_name ??
              user?.username ??
              "Unknown User",

            email:
              user?.email ??
              "",

            avatar: "",
          }}
        />

      </SidebarFooter>

    </Sidebar>

  )
}