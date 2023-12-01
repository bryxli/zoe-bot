import { NextjsSite, StackContext } from "sst/constructs";
import * as config from "../config.json";

export function WebStack({ stack }: StackContext) {
  const site = new NextjsSite(stack, "frontend", {
    path: "packages/frontend",
    environment: {
      APPLICATION_ID: config.application_id,
    },
  });

  stack.addOutputs({
    URL: site.url,
  });
}
