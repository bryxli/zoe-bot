import { NextRequest, NextResponse } from "next/server";

export const dynamic = "force-dynamic"; // defaults to force-static
export async function GET(request: NextRequest) {
  return new NextResponse(
    "calls discord guilds endpoint using params from request body",
  );
}
