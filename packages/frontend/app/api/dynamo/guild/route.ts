import { NextRequest, NextResponse } from "next/server";

import { getGuild } from "@/api/dynamo/dynamo";

export const dynamic = "force-dynamic";

export async function POST(request: NextRequest) {
  const body = await request.json();
  const guild = await getGuild(body.guildId);
  guild.guild_id = guild.guild_id?.toString();
  return NextResponse.json(guild);
}
