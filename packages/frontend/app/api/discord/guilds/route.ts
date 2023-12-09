import { NextRequest, NextResponse } from "next/server";

export const dynamic = "force-dynamic"; // defaults to force-static
export async function POST(request: NextRequest) {
  /*
  fetch("https://discord.com/api/users/@me/guilds", {
    headers: {
      authorization: `${tokenType} ${accessToken}`,
    },
  })
    .then((result) =>
      result.status === 429 ? Promise.resolve("429") : result.json(),
    )
    .then((response) => {
      if (response != 429) {
        processGuilds(response);
        router.push("/dashboard");
      }
    })
    .catch(console.error);
  */
  return NextResponse.json(["test", "test2"]);
}
