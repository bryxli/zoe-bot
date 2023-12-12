import { NextRequest, NextResponse } from "next/server";

import { destroyGuild } from "../dynamo";

export const dynamic = "force-dynamic"; // defaults to force-static

export async function POST(request: NextRequest) {
  const res = await request.json();
  const guild = await destroyGuild(res.guild);

  return NextResponse.json(guild);
}
