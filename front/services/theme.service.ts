import api from "@/lib/axios";

export interface Theme {
  id: string;

  name: string;
  description: string | null;
  type: string;

  sidebar_background_color: string;
  sidebar_foreground_color: string;

  topbar_background_color: string;
  topbar_foreground_color: string;

  card_header_background_color: string;
  card_header_foreground_color: string;

  table_header_background_color: string;
  table_header_foreground_color: string;

  border_color: string;

  is_default: boolean;
  is_active: boolean;
}

export interface UpdateThemeRequest {
  sidebar_background_color: string;
  sidebar_foreground_color: string;

  topbar_background_color: string;
  topbar_foreground_color: string;

  card_header_background_color: string;
  card_header_foreground_color: string;

  table_header_background_color: string;
  table_header_foreground_color: string;

  border_color: string;
}

export async function getThemes() {
  const { data } = await api.get<Theme[]>("/themes");
  return data;
}

export async function getTheme(
  id: string,
) {
  const { data } = await api.get<Theme>(
    `/themes/${id}`,
  );

  return data;
}

export async function updateTheme(
  id: string,
  payload: UpdateThemeRequest,
) {
  const { data } = await api.put<Theme>(
    `/themes/${id}`,
    payload,
  );

  return data;
}