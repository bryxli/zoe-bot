import { NextRequest, NextResponse } from "next/server";
import { findByAccountId } from "../league";

export const dynamic = "force-dynamic"; // defaults to force-static

export async function POST(request: NextRequest) {
  const body = await request.json();
  const summoner = await findByAccountId(body.accountId, body.region);
  return NextResponse.json(summoner);
}
