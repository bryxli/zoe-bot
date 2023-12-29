"use client";

import { Fragment, useContext, useEffect } from "react";
import { Container } from "react-bootstrap";

import Header from "@/components/Header";
import Information from "@/components/Information";
import { AuthContext } from "@/contexts/AuthContext";

export default function Home() {
  const authContext = useContext(AuthContext);
  const { signOut } = authContext;

  useEffect(() => {
    const startup = async () => {
      await fetch("/api/startup", {
        method: "POST",
      });
    };

    startup();
    signOut();
  }, [signOut]);

  return (
    <div data-testid="Home">
      <Container>
        <Header />
        <section className="readable">
          <Information />
          {/** Output */}
        </section>
      </Container>
    </div>
  );
}
