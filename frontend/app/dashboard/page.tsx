"use client";

import { useContext, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Col, Container, Row } from "react-bootstrap";

import { GuildProps } from "../types";

import User from "../components/User";
import SearchBox from "../components/SearchBox";
import Guild from "../components/Guild";
import { AuthContext } from "../contexts/AuthContext";

export default function Dashboard() {
  const router = useRouter();
  const authContext = useContext(AuthContext);
  const [guilds, setGuilds] = useState<GuildProps[]>([]);
  const [adminGuilds, setAdminGuilds] = useState<GuildProps[]>([]);
  const { signIn, userInfo } = authContext;

  useEffect(() => {
    const fragment = new URLSearchParams(window.location.hash.slice(1));
    const [accessToken, tokenType] = [
      fragment.get("access_token"),
      fragment.get("token_type"),
    ];

    if (!accessToken) {
      router.push("/");
    }

    !userInfo &&
      fetch("https://discord.com/api/users/@me", {
        headers: {
          authorization: `${tokenType} ${accessToken}`,
        },
      })
        .then((result) => result.json())
        .then((response) => {
          const { username, avatar, id } = response;
          signIn({ username, avatar, id });
        })
        .catch(console.error);

    fetch("https://discord.com/api/users/@me/guilds", {
      headers: {
        authorization: `${tokenType} ${accessToken}`,
      },
    })
      .then((result) =>
        result.status === 429 ? Promise.reject("429") : result.json(),
      )
      .then((response) => setGuilds(response))
      .catch(console.error);
  }, [router, signIn, userInfo]);

  useEffect(() => {
    setAdminGuilds(guilds.filter((guild: GuildProps) => guild.owner));
  }, [guilds]);

  return (
    <Container className="mt-3">
      {userInfo && <User {...userInfo} />}
      {adminGuilds.length > 0 && (
        <Row>
          {adminGuilds.map((guild) => (
            <Col key={guild.id}>
              {" "}
              <Guild {...guild} />{" "}
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