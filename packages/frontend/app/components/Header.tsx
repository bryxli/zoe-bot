"use client";

import { useContext, useEffect, useState } from "react";
import { Button, Container } from "react-bootstrap";

import { AuthContext } from "../contexts/AuthContext";
import { useRouter } from "next/navigation";

export default function Header() {
  const router = useRouter();
  const authContext = useContext(AuthContext);
  const { userInfo } = authContext;
  const [applicationId, setApplicationId] = useState<string | undefined>(undefined);

  const redirect = "https://ddwebabika1cp.cloudfront.net"; // TODO: update readme for redirect instructions
  const href = `https://discord.com/api/oauth2/authorize?client_id=${applicationId}&redirect_uri=${redirect}/load&response_type=token&scope=guilds%20identify`;

  useEffect(() => {
    setApplicationId(process.env.APPLICATION_ID);
  }, [setApplicationId]);

  const handleLogout = async () => {
    router.push("/");
  };

  const renderLoginButton = () => (
    applicationId !== undefined && 
      <Button className="authButton" href={href}>
        Login with Discord
      </Button>
  );

  return (
    <Container className="d-flex flex-column align-items-center justify-content-center mb-4">
      <header className="font">zoe, the aspect of twighlight</header>
      {
        userInfo ? (
          <Button className="authButton" onClick={handleLogout}>
            Logout
          </Button>
        ) : renderLoginButton()
      }
    </Container>
  );
}
