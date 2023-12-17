import { NextRequest, NextResponse } from "next/server";

import { createGuild } from "../dynamo";

export const dynamic = "force-dynamic"; // defaults to force-static

export async function POST(request: NextRequest) {
  const res = await request.json();
  const guild = await createGuild(res.id, res.webhook.id, res.webhook.url);

  return NextResponse.json(guild);
}
