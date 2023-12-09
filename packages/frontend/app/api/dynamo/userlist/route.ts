import { NextRequest, NextResponse } from "next/server";
import { getAllUsers } from "../dynamo";

export const dynamic = "force-dynamic"; // defaults to force-static

export async function POST(request: NextRequest) {
  const body = await request.json();
  const userlist = await getAllUsers(body.guildId);

  return NextResponse.json(userlist);
}
