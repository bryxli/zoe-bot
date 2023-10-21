"use client";

import { createContext, useEffect, useState } from "react";

import {
  GuildContextData,
  GuildProps,
  ProviderProps,
  UserProps,
} from "../types";

export const GuildContext = createContext({} as GuildContextData);

export function AuthProvider({ children }: ProviderProps) {
  const [guilds, setGuilds] = useState<GuildProps[]>([]);
  const [adminGuilds, setAdminGuilds] = useState<GuildProps[]>([]);

  useEffect(() => {
    setAdminGuilds(guilds.filter((guild: GuildProps) => guild.owner));
  }, [guilds]);

  const processGuilds = (props: GuildProps[]) => {
    setGuilds(props);
  };

  return (
    <GuildContext.Provider value={{ processGuilds, guilds, adminGuilds }}>
      {children}
    </GuildContext.Provider>
  );
}
