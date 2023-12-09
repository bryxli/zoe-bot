import { NextRequest, NextResponse } from "next/server";

export const dynamic = "force-dynamic"; // defaults to force-static

export async function POST(request: NextRequest) {
  const body = await request.json();

  const res = await fetch("https://discord.com/api/users/@me", {
    headers: {
      authorization: `${body.tokenType} ${body.accessToken}`,
    },
  })
    .then((result) => result.json())
    .then((response) => {
      return response;
    });
  return NextResponse.json(res);
}
