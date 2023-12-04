import { NextjsSite, StackContext } from "sst/constructs";
import * as devConfig from "../config-dev.json";
import * as prodConfig from "../config-prod.json";

export function WebStack({ app, stack }: StackContext) {
  const currentConfig = app.stage === "prod" ? prodConfig : devConfig;

  const site = new NextjsSite(stack, "frontend", {
    path: "packages/frontend",
    environment: {
      APPLICATION_ID: currentConfig.application_id,
    },
  });

  stack.addOutputs({
    URL: site.url,
  });
}
