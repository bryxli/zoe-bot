"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import User from "../components/User";
import SearchBox from "../components/SearchBox";

interface Guild {
  id: string;
  name: string;
  icon: null | string;
  owner: boolean;
  permissions: number;
  permissions_new: string;
  features: string[];
}

export default function Dashboard() {
  const router = useRouter();
  const [userInfo, setUserInfo] = useState({
    username: "",
    avatar: "",
    id: "",
  });
  const [guilds, setGuilds] = useState([]);

  useEffect(() => {
    const fragment = new URLSearchParams(window.location.hash.slice(1));
    const [accessToken, tokenType] = [
      fragment.get("access_token"),
      fragment.get("token_type"),
    ];

    if (!accessToken) {
      router.push("/");
    }

    fetch("https://discord.com/api/users/@me", {
      headers: {
        authorization: `${tokenType} ${accessToken}`,
      },
    })
      .then((result) => result.json())
      .then((response) => {
        const { username, avatar, id } = response;
        setUserInfo({ username, avatar, id });
      })
      .catch(console.error);

    fetch("https://discord.com/api/users/@me/guilds", {
      headers: {
        authorization: `${tokenType} ${accessToken}`,
      },
    })
      .then((result) => result.json())
      .then((response) => {
        !response.hasOwnProperty("message") && setGuilds(response);
      })
      .catch(console.error);
  }, [router]);

  useEffect(() => {
    const adminGuilds = guilds.filter((guild: Guild) => guild.owner); // Filter for admin guilds
    adminGuilds.forEach((guild: Guild) => {
      console.log(guild);
    });
  }, [guilds]);

  return (
    <>
      <User
        username={userInfo.username}
        avatar={userInfo.avatar}
        id={userInfo.id}
      />
      <SearchBox />
    </>
  );
}
