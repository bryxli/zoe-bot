import { NextRequest, NextResponse } from "next/server";

import { acknowledge } from "@/api/dynamo/dynamo";

export const dynamic = "force-dynamic";

export async function POST(request: NextRequest) {
  const res = await request.json();
  const guild = await acknowledge(res.guild);

  return NextResponse.json(guild);
}
