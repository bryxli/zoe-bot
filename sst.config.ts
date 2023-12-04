import { SSTConfig } from "sst";
import { InfraStack } from "./stacks/InfraStack";
import { BotStack } from "./stacks/BotStack";
import { WebStack } from "./stacks/WebStack";
import * as config from "./config.json";

export default {
  config(_input) {
    return {
      name: "zoe-bot",
      region: config.aws_region,
    };
  },
  stacks(app) {
    app.stack(InfraStack).stack(BotStack);
    app.stage === "prod" && app.stack(WebStack); // Currently only deploys web app to prod
  },
} satisfies SSTConfig;
