"use client";

import { useContext, useEffect } from "react";
import { useRouter } from "next/navigation";

import { AuthContext } from "../contexts/AuthContext";
import { GuildContext } from "../contexts/GuildContext";
import Header from "../components/Header";

export default function Load() {
  const router = useRouter();
  const authContext = useContext(AuthContext);
  const guildContext = useContext(GuildContext);
  const { signIn, userInfo } = authContext;
  const { processGuilds } = guildContext;

  useEffect(() => {
    const fragment = new URLSearchParams(window.location.hash.slice(1));
    const [accessToken, tokenType] = [
      fragment.get("access_token"),
      fragment.get("token_type"),
    ];

    const fetchData = async () => {
      if (!userInfo) {
        await fetch("/api/discord/user", {
          method: "POST",
          body: JSON.stringify({
            tokenType: tokenType,
            accessToken: accessToken,
          }),
        })
          .then((result) => result.json())
          .then((response) => {
            signIn(response);
          });
      } else {
        await fetch("/api/discord/guilds", {
          method: "POST",
          body: JSON.stringify({
            tokenType: tokenType,
            accessToken: accessToken,
          }),
        })
          .then((result) => result.json())
          .then((response) => {
            if (response !== "429") {
              processGuilds(response);
              router.push("/dashboard");
            }
          });
      }
    };

    !accessToken && router.push("/");

    fetchData();
  }, [processGuilds, router, signIn, userInfo]);

  return (
    <>
      <Header />
    </>
  );
}
