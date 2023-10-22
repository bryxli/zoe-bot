"use client";

import { useContext, useEffect } from "react";
import { Container } from "react-bootstrap";

import Header from "./components/Header";
import { AuthContext } from "./contexts/AuthContext";

export default function Home() {
  const authContext = useContext(AuthContext);
  const { signOut } = authContext;

  useEffect(() => {
    signOut();
  }, [signOut]);

  return (
    <Container className="mt-3">
      <Header />
      {/** Information */}
      {/** Output */}
    </Container>
  );
}
