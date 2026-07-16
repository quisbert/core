import api from "@/lib/axios";

export interface OrganizationSetting {
  id: string;

  organization_name: string;
  organization_abbreviation: string | null;

  system_name: string;
  system_abbreviation: string | null;

  logo_id: string | null;
  favicon_id: string | null;
  login_background_id: string | null;

  email: string | null;
  phone: string | null;
  website: string | null;
  address: string | null;

  timezone: string;
  language: string;

  login_message: string | null;

  theme_id: string;

  is_active: boolean;
}

export interface UpdateOrganizationRequest {
  organization_name: string;
  organization_abbreviation: string | null;

  system_name: string;
  system_abbreviation: string | null;

  logo_id: string | null;
  favicon_id: string | null;
  login_background_id: string | null;

  email: string | null;
  phone: string | null;
  website: string | null;
  address: string | null;

  timezone: string;
  language: string;

  login_message: string | null;

  theme_id: string;
}

export async function getOrganization() {
  const { data } =
    await api.get<OrganizationSetting>(
      "/organization-settings",
    );

  return data;
}

export async function updateOrganization(
  payload: UpdateOrganizationRequest,
) {
  const { data } =
    await api.put<OrganizationSetting>(
      "/organization-settings",
      payload,
    );

  return data;
}