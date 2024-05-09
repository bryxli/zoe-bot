import { NextjsSite, StackContext, use } from "sst/constructs";
import * as config from "../configs/config.json";
import { InfraStack } from "./InfraStack";

export function WebStack({ app, stack }: StackContext) {
  const { table } = use(InfraStack);

  const site = new NextjsSite(stack, "frontend", {
    path: "packages/frontend",
    environment: { // TODO: create url env var from file
      APPLICATION_ID: config.application_id,
      RIOT_API_KEY: config.riot_key,
      TOKEN: config.token,
    },
    bind: [table],
  });

  stack.addOutputs({
    URL: site.url,
  });
}
