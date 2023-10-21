"use client";

import { createContext, useContext, useState, ReactNode } from "react";

import { UserProps } from "../types";

interface SignInParams {
  username: string;
  avatar: string;
  id: string;
}

interface AuthContextData {
  signIn: (params: SignInParams) => void;
  signOut: () => void;
  userInfo: UserProps | null;
}

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthContext = createContext({} as AuthContextData);

export function AuthProvider({ children }: AuthProviderProps) {
  const [userInfo, setUserInfo] = useState<UserProps | null>(null);

  const signIn = ({ username, avatar, id }: SignInParams) =>
    setUserInfo({ username, avatar, id });

  const signOut = () => setUserInfo(null);

  return (
    <AuthContext.Provider value={{ signIn, signOut, userInfo }}>
      {children}
    </AuthContext.Provider>
  );
}
