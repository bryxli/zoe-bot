import { NextRequest, NextResponse } from "next/server";

import { findByAccountId } from "@/api/league/league";

export const dynamic = "force-dynamic";

export async function POST(request: NextRequest) {
  const body = await request.json();
  const summoner = await findByAccountId(body.accountId, body.region);
  return NextResponse.json(summoner);
}
