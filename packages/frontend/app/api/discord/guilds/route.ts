import { NextRequest, NextResponse } from "next/server";

export const dynamic = "force-dynamic";

export async function POST(request: NextRequest) {
  const body = await request.json();

  const res = await fetch("https://discord.com/api/users/@me/guilds", {
    headers: {
      authorization: `${body.tokenType} ${body.accessToken}`,
    },
  })
    .then((result) =>
      result.status === 429 ? Promise.resolve("429") : result.json(),
    )
    .then((response) => {
      return response;
    });
  return NextResponse.json(res);
}
