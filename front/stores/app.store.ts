"use client";

import { create } from "zustand";

import {
  getOrganization,
  type OrganizationSetting,
} from "@/services/organization.service";

import {
  getTheme,
  type Theme,
} from "@/services/theme.service";

interface AppState {
  organization: OrganizationSetting | null;

  theme: Theme | null;

  isLoading: boolean;

  load: () => Promise<void>;
}

export const useAppStore =
create<AppState>((set) => ({

  organization: null,

  theme: null,

  isLoading: false,

  load: async () => {

    set({
      isLoading: true,
    });

    try {

      const organization =
        await getOrganization();

      const theme =
        await getTheme(
          organization.theme_id,
        );

      set({

        organization,

        theme,

        isLoading: false,

      });

    } catch {

      set({

        organization: null,

        theme: null,

        isLoading: false,

      });

    }

  },

}));