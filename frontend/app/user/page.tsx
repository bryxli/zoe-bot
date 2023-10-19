"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";

export default function User() {
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
      <Image
        src={`https://cdn.discordapp.com/avatars/${userInfo.id}/${userInfo.avatar}.jpg`}
        alt="User Avatar"
        width={150}
        height={150}
      />
      <p>
        You have successfully signed in as <b>{userInfo.username}</b>
      </p>
    </>
  );
}
