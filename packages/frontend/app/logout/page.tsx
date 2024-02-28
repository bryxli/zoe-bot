"use client";

import { useContext, useEffect } from "react";
import { Button, Container, Row } from "react-bootstrap";

import "../app.css";

import { AuthContext } from "@/contexts/AuthContext";

export default function Home() {
  const authContext = useContext(AuthContext);
  const { signOut } = authContext;

  useEffect(() => {
    signOut();
  }, []);

  return (
    <div data-testid="Logout">
      <Container className="d-flex flex-column align-items-center justify-content-center mb-4">
        <Row className="font">You have been signed out.</Row>
        <Button className="authButton" href="/">
          Home
        </Button>
      </Container>
    </div>
  );
}
