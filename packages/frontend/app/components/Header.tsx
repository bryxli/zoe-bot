"use client";

import { useContext } from "react";
import { Button, Container } from "react-bootstrap";

import { AuthContext } from "../contexts/AuthContext";

export default function Header() {
  const authContext = useContext(AuthContext);
  const { userInfo } = authContext;

  // const application_id = process.env.APPLICATION_ID;
  // const redirect = "https://d1pi4zyx1ge8ej.cloudfront.net/load"; // Update with Cloudfront URL
  const application_id = "1154647072138608694";
  const redirect = "http://localhost:3000/load";
  const href = `https://discord.com/api/oauth2/authorize?client_id=${application_id}&redirect_uri=${encodeURIComponent(
    redirect,
  )}&response_type=token&scope=guilds%20identify`;

  return (
    <Container className="d-flex flex-column align-items-center justify-content-center mb-4">
      <header className="font">zoe, the aspect of twighlight</header>
      {userInfo ? (
        <Button className="authButton" href="/logout">
          Logout
        </Button>
      ) : (
        <Button className="authButton" href={href}>
          Login with Discord
        </Button>
      )}
    </Container>
  );
}
