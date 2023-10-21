"use client";

import { useContext, useEffect } from "react";

import { AuthContext } from "./contexts/AuthContext";

export default function Home() {
  const authContext = useContext(AuthContext);
  const { signOut } = authContext;

  useEffect(() => {
    signOut();
  }, [signOut]);

  return (
    <>
      {/** Information */}
      {/** Output */}
    </>
  );
}
