"use client";

import { useContext, useEffect } from "react";
import { Col, Container, Row } from "react-bootstrap";
import { useRouter } from "next/navigation";

import User from "../components/User";
import SearchBox from "../components/SearchBox";
import Guild from "../components/Guild";
import Header from "../components/Header";
import { AuthContext } from "../contexts/AuthContext";
import { GuildContext } from "../contexts/GuildContext";

export default function Dashboard() {
  const router = useRouter();
  const authContext = useContext(AuthContext);
  const guildContext = useContext(GuildContext);
  const { userInfo } = authContext;
  const { adminGuilds } = guildContext;

  useEffect(() => {
    !userInfo && router.push("/");
  }, [router, userInfo]);

  return (
    <Container className="mt-3">
      <Header />
      {userInfo && <User {...userInfo} />}
      {adminGuilds && adminGuilds.length > 0 && (
        <Row>
          {adminGuilds.map((guild) => (
            <Col key={guild.id}>
              <Guild {...guild} />
            </Col>
          ))}
        </Row>
      )}
      <Row className="mt-3">
        <SearchBox />
      </Row>
    </Container>
  );
}
