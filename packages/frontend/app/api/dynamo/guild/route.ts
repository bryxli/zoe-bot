import { NextRequest, NextResponse } from "next/server";
import { getGuild } from "../dynamo";

export const dynamic = "force-dynamic"; // defaults to force-static

export async function POST(request: NextRequest) {
  const body = await request.json();
  const guild = await getGuild(body.guildId);
  guild.guild_id = guild.guild_id?.toString();
  return NextResponse.json(guild);
}
