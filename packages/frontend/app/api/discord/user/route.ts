import { NextRequest, NextResponse } from "next/server";

export const dynamic = "force-dynamic"; // defaults to force-static

export async function POST(request: NextRequest) {
  // return {username, avatar, id}
  /*
  fetch("https://discord.com/api/users/@me", {
    headers: {
      authorization: `${tokenType} ${accessToken}`,
    },
  })
    .then((result) => result.json())
    .then((response) => {
      return response;
    })
    .catch(console.error);
  */
  return NextResponse.json({ username: "test", avatar: "test", id: "test" });
}
