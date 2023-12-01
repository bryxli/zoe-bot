"use client";

import { createContext, useState } from "react";

import { AuthContextData, ProviderProps, UserProps } from "../types";

export const AuthContext = createContext({} as AuthContextData);

export function AuthProvider({ children }: ProviderProps) {
  const [userInfo, setUserInfo] = useState<UserProps | null>(null);

  const signIn = ({ username, avatar, id }: UserProps) =>
    setUserInfo({ username, avatar, id });

  const signOut = () => setUserInfo(null);

  return (
    <AuthContext.Provider value={{ signIn, signOut, userInfo }}>
      {children}
    </AuthContext.Provider>
  );
}
