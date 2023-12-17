import { NextRequest, NextResponse } from "next/server";

export const dynamic = "force-dynamic"; // defaults to force-static

export async function POST(request: NextRequest) {
  const body = await request.json();

  const res = await fetch(
    `https://discordapp.com/api/channels/${body.id}/webhooks`,
    {
      method: "POST",
      headers: {
        Authorization: `Bot ${process.env.TOKEN}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: "zœ",
      }),
    },
  ).then((result) => result.json());
  return NextResponse.json({ id: res.id, url: res.url });
}

export async function DELETE(request: NextRequest) {
  const body = await request.json();

  const res = await fetch(
    `https://discordapp.com/api/webhooks/${body.guild.webhook_id}`,
    {
      method: "DELETE",
      headers: {
        Authorization: `Bot ${process.env.TOKEN}`,
      },
    },
  );

  return NextResponse.json(res);
}
