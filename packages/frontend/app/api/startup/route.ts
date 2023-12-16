import { NextResponse } from "next/server";

export const dynamic = "force-dynamic"; // defaults to force-static

export async function POST() {
  return NextResponse.json("api started");
}
