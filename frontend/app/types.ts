import { ReactNode } from "react";

export interface AuthContextData {
  signIn: (params: UserProps) => void;
  signOut: () => void;
  userInfo: UserProps | null;
}

export interface AuthProviderProps {
  children: ReactNode;
}

export interface UserProps {
  username: string;
  avatar: string;
  id: string;
}

export interface GuildProps {
  id: string;
  name: string;
  icon: null | string;
  owner: boolean;
  permissions: number;
  permissions_new: string;
  features: string[];
}
