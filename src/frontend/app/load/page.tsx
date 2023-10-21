"use client";

import { useContext, useEffect } from "react";
import { useRouter } from "next/navigation";

import { AuthContext } from "../contexts/AuthContext";
import { GuildContext } from "../contexts/GuildContext";

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

    !accessToken && router.push("/");

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

    userInfo &&
      fetch("https://discord.com/api/users/@me/guilds", {
        headers: {
          authorization: `${tokenType} ${accessToken}`,
        },
      })
        .then((result) =>
          result.status === 429 ? Promise.resolve("429") : result.json(),
        )
        .then((response) => {
          if (response != 429) {
            processGuilds(response);
            router.push("/dashboard");
          }
        })
        .catch(console.error);
  }, [processGuilds, router, signIn, userInfo]);

  return <></>;
}
