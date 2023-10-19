"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

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
        console.log(response);
        const { username, avatar, id } = response;
        setUserInfo({ username, avatar, id });
      })
      .catch(console.error);
  }, [router]);

  return (
    <>
      <h1>{userInfo.username}</h1>
    </>
  );
}
