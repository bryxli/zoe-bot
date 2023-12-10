"use client";

import { useContext, useEffect } from "react";
import { Container } from "react-bootstrap";
import Header from "./components/Header";
import Information from "./components/Information";
import { AuthContext } from "./contexts/AuthContext";

export default function Home() {
  const authContext = useContext(AuthContext);
  const { signOut } = authContext;

  useEffect(() => {
    const startup = async () => {
      await fetch("/api/startup");
    };

    startup();
    signOut();
  }, [signOut]);

  return (
    <Container className="mt-3">
      <Header />
      <section className="readable">
        <Information />
        {/** Output */}
      </section>
    </Container>
  );
}
