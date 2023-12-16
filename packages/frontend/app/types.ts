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
  guild: DynamoGuildProps;
  setGuild: (guild: DynamoGuildProps) => void;
  summoners: SummonerProps[];
}

export interface DynamoGuildProps {
  acknowledgment: boolean;
  guild_id: string;
  region: string;
  userlist: Record<string, string>[];
  webhook_id: string;
  webhook_url: string;
}

export interface GuildCommandsProps {
  guild: DynamoGuildProps;
  setGuild: (guild: DynamoGuildProps) => void;
  setData: (data: DataProps) => void;
}

export interface UserListProps {
  summoners: SummonerProps[];
  setGuild: (guild: DynamoGuildProps) => void;
  setData: (data: DataProps) => void;
}

export interface SummonerProps {
  id: string;
  accountId: string;
  puuid: string;
  name: string;
  profileIconId: number;
  revisionDate: number;
  summonerLevel: number;
}

export interface SummonerComponentProps {
  summoner: SummonerProps;
  setData: (data: DataProps) => void;
}

export interface SummonerModalProps {
  showModal: boolean;
  onHide: () => void;
  summoner: SummonerProps;
}

export interface DataProps {
  command: string;
  body: string;
}
