"use client";

import { useContext } from "react";
import { Button, Container } from "react-bootstrap";

import { AuthContext } from "../contexts/AuthContext";
import { useRouter } from "next/navigation";

export default function Header() {
  const router = useRouter();
  const authContext = useContext(AuthContext);
  const { userInfo } = authContext;

  const application_id = process.env.APPLICATION_ID;
  const redirect = "https://d3br3pj7y7nksb.cloudfront.net/load"; // TODO: update readme for redirect instructions
  const href = `https://discord.com/api/oauth2/authorize?client_id=${application_id}&redirect_uri=${redirect}&response_type=token&scope=guilds%20identify`;

  const handleLogout = async () => {
    router.push("/");
  };

  return (
    <Container className="d-flex flex-column align-items-center justify-content-center">
      <header>zoe, the aspect of twighlight</header>
      {userInfo ? (
        <Button onClick={handleLogout}>Logout</Button>
      ) : (
        <Button href={href}>Login with Discord</Button>
      )}
    </Container>
  );
}
