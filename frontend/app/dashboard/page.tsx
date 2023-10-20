"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import User from "../components/User";
import SearchBox from "../components/SearchBox";

export default function Dashboard() {
  const router = useRouter();
  const [userInfo, setUserInfo] = useState({
    username: "",
    avatar: "",
    id: "",
  });

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
  }, [router]);

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
