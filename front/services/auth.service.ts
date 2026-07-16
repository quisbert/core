import api from "@/lib/axios";

import type {
  CurrentUser,
  LoginCredentials,
  TokenResponse,
} from "@/types/auth";

export async function login(
  credentials: LoginCredentials,
): Promise<TokenResponse> {
  const body = new URLSearchParams();

  body.append(
    "username",
    credentials.username,
  );

  body.append(
    "password",
    credentials.password,
  );

  const response = await api.post<TokenResponse>(
    "/auth/login",
    body,
    {
      headers: {
        "Content-Type":
          "application/x-www-form-urlencoded",
      },
    },
  );

  return response.data;
}

export async function getCurrentUser(): Promise<CurrentUser> {
  const response = await api.get<CurrentUser>(
    "/auth/me",
  );

  return response.data;
}

export async function refreshToken(
  refreshToken: string,
): Promise<TokenResponse> {
  const response = await api.post<TokenResponse>(
    "/auth/refresh",
    {
      refresh_token: refreshToken,
    },
  );

  return response.data;
}

export async function logout(): Promise<void> {
  try {
    await api.post("/auth/logout");
  } finally {
    localStorage.removeItem(
      "access_token",
    );

    localStorage.removeItem(
      "refresh_token",
    );

    localStorage.removeItem(
      "auth-storage",
    );
  }
}