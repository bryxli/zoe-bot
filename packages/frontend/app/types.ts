import { ReactNode } from "react";

export interface ProviderProps {
  children: ReactNode;
}

export interface AuthContextData {
  signIn: (params: UserProps) => void;
  signOut: () => void;
  userInfo: UserProps | null;
}

export interface GuildContextData {
  processGuilds: (params: GuildProps[]) => void;
  guilds: GuildProps[];
  adminGuilds: GuildProps[];
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

export interface GuildModalProps {
  showModal: boolean;
  onHide: () => void;
  id: string;
  name: string;
  icon: string | null;
}
