"use client";

import { Fragment, useContext, useEffect, useRef } from "react";
import { Container } from "react-bootstrap";

import Header from "@/components/Header";
import Information from "@/components/Information";
import { AuthContext } from "@/contexts/AuthContext";

export default function Home() {
  const authContext = useContext(AuthContext);
  const { signOut } = authContext;

  const isFirstRender = useRef(true);

  useEffect(() => {
    const startup = async () => {
      await fetch("/api/startup", {
        method: "POST",
      });
    };

    if (!isFirstRender.current) {
      startup();
      signOut();
    } else {
      isFirstRender.current = false;
    }
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
