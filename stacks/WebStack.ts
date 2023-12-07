import { NextjsSite, StackContext, use } from "sst/constructs";
import * as devConfig from "../configs/config-dev.json";
import * as prodConfig from "../configs/config-prod.json";
import { InfraStack } from "./InfraStack";

export function WebStack({ app, stack }: StackContext) {
  const { table } = use(InfraStack);

  const currentConfig = app.stage === "prod" ? prodConfig : devConfig;

  const site = new NextjsSite(stack, "frontend", {
    path: "packages/frontend",
    environment: {
      APPLICATION_ID: currentConfig.application_id,
    },
    bind: [table],
  });

  stack.addOutputs({
    URL: site.url,
  });
}
