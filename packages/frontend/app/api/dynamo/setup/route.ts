import { NextRequest, NextResponse } from "next/server";

import { createGuild } from "@/api/dynamo/dynamo";

export const dynamic = "force-dynamic";

export async function POST(request: NextRequest) {
  const res = await request.json();
  const guild = await createGuild(res.id, res.webhook.id, res.webhook.url);

  return NextResponse.json(guild);
}
