export interface LoginCredentials {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface CurrentUser {
  id: string;
  username: string;
  email: string;
  is_active: boolean;
  roles: string[];
  permissions: string[];
}