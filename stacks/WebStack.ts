import { NextjsSite, StackContext, use } from "sst/constructs";
import fs from "fs/promises";
import * as config from "../configs/config.json";
import { InfraStack } from "./InfraStack";

export async function WebStack({ app, stack }: StackContext) {
  const { table } = use(InfraStack);

  if (app.stage !== "dev") {
    async function loadEnvironment() {
      const defaultEnv = {
        APPLICATION_ID: config.application_id,
        RIOT_API_KEY: config.riot_key,
        TOKEN: config.token,
      };

      try {
        const data = await fs.readFile("deploy-prod.json", "utf-8");
        const deployConfig = JSON.parse(data);

        return { ...defaultEnv, URL: deployConfig.URL };
      } catch (err) {
        return { ...defaultEnv, URL: "" };
      }
    }

    const site = new NextjsSite(stack, "frontend", {
      path: "packages/frontend",
      environment: await loadEnvironment(),
      bind: [table],
    });

    stack.addOutputs({
      URL: site.url,
    });
  }
}
