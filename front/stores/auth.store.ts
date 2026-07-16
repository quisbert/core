"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

import {
  getCurrentUser,
  login,
  logout,
} from "@/services/auth.service";

import type {
  CurrentUser,
  LoginCredentials,
} from "@/types/auth";

interface AuthState {
  user: CurrentUser | null;

  isAuthenticated: boolean;

  isLoading: boolean;

  error: string | null;

  signIn: (
    credentials: LoginCredentials,
  ) => Promise<void>;

  loadUser: () => Promise<void>;

  signOut: () => Promise<void>;

  clearError: () => void;

  can: (
    permission: string,
  ) => boolean;
}

export const useAuthStore =
create<AuthState>()(

  persist(

    (set, get) => ({

      user: null,

      isAuthenticated: false,

      isLoading: false,

      error: null,

      signIn: async (
        credentials,
      ) => {

        set({
          isLoading: true,
          error: null,
        });

        try {

          const tokens =
            await login(credentials);

          localStorage.setItem(
            "access_token",
            tokens.access_token,
          );

          localStorage.setItem(
            "refresh_token",
            tokens.refresh_token,
          );

          const user =
            await getCurrentUser();

          set({

            user,

            isAuthenticated: true,

            isLoading: false,

            error: null,

          });

        } catch {

          set({

            user: null,

            isAuthenticated: false,

            isLoading: false,

            error:
              "Invalid username or password.",

          });

          throw new Error(
            "Authentication failed.",
          );

        }

      },

      loadUser: async () => {

        const token =
          localStorage.getItem(
            "access_token",
          );

        if (!token) {

          set({

            user: null,

            isAuthenticated: false,

          });

          return;

        }

        try {

          const user =
            await getCurrentUser();

          set({

            user,

            isAuthenticated: true,

          });

        } catch {

          await logout();

          set({

            user: null,

            isAuthenticated: false,

          });

        }

      },

      signOut: async () => {

        await logout();

        set({

          user: null,

          isAuthenticated: false,

          isLoading: false,

          error: null,

        });

      },

      clearError: () => {

        set({

          error: null,

        });

      },

      can: (
        permission,
      ) => {

        return (

          get()
            .user
            ?.permissions
            .includes(permission)

          ?? false

        );

      },

    }),

    {

      name: "auth-storage",

      partialize: (
        state,
      ) => ({

        user: state.user,

        isAuthenticated:
          state.isAuthenticated,

      }),

    },

  ),

);