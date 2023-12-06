"use client";

import { useContext, useEffect } from "react";
import { Button, Container, Row } from "react-bootstrap";

import { AuthContext } from "../contexts/AuthContext";

import "../app.css";

export default function Home() {
  const authContext = useContext(AuthContext);
  const { signOut } = authContext;

  useEffect(() => {
    signOut();
  }, [signOut]);

  return (
    <Container className="d-flex flex-column align-items-center justify-content-center mb-4">
      <Row className="font">You have been signed out.</Row>
      <Button className="authButton" href="/">
        Home
      </Button>
    </Container>
  );
}
