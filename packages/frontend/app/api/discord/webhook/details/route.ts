import { NextRequest, NextResponse } from "next/server";

export const dynamic = "force-dynamic"; // defaults to force-static

export async function POST(request: NextRequest) {
  const body = await request.json();

  const webhook = await fetch(
    `https://discordapp.com/api/webhooks/${body.guild.webhook_id}`,
    {
      headers: {
        Authorization: `Bot ${process.env.TOKEN}`,
      },
    },
  ).then((result) => result.json());

  const channel = await fetch(
    `https://discordapp.com/api/channels/${webhook.channel_id}`,
    {
      headers: {
        Authorization: `Bot ${process.env.TOKEN}`,
      },
    },
  ).then((result) => result.json());

  return NextResponse.json(channel.name);
}
