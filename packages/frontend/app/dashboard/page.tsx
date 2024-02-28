"use client";

import { useContext, useEffect } from "react";
import { Col, Container, Row } from "react-bootstrap";
import { useRouter } from "next/navigation";

import User from "@/components/User";
import SearchBox from "@/components/SearchBox";
import Guild from "@/components/guild/Guild";
import Header from "@/components/Header";
import { AuthContext } from "@/contexts/AuthContext";
import { GuildContext } from "@/contexts/GuildContext";

export default function Dashboard() {
  const router = useRouter();
  const authContext = useContext(AuthContext);
  const guildContext = useContext(GuildContext);
  const { userInfo } = authContext;
  const { adminGuilds } = guildContext;

  useEffect(() => {
    !userInfo && router.push("/logout");
  }, [userInfo]);

  return (
    <div data-testid="Dashboard">
      <Header />
      {userInfo && (
        <Container
          className="d-flex flex-column align-items-center justify-content-center readable pt-2 pb-2"
          style={{ textAlign: "center" }}
        >
          <User {...userInfo} />
          {adminGuilds && adminGuilds.length > 0 && (
            <Row>
              {adminGuilds.map((guild) => (
                <Col key={guild.id}>
                  <Guild {...guild} />
                </Col>
              ))}
            </Row>
          )}
          {/*
          <Row className="mt-3">
            <SearchBox />
          </Row>
          */}
        </Container>
      )}
    </div>
  );
}
