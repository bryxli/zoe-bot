import { NextRequest, NextResponse } from "next/server";

import { acknowledge } from "../dynamo";

export const dynamic = "force-dynamic"; // defaults to force-static

export async function POST(request: NextRequest) {
  const res = await request.json();
  await acknowledge(res.guild);

  return NextResponse.json("");
}
