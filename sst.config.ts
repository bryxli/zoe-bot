import { SSTConfig } from "sst";
import { InfraStack } from "./stacks/InfraStack";
import { BotStack } from "./stacks/BotStack";
import { WebStack } from "./stacks/WebStack";
import * as config from "./config.json";

export default {
  config(_input) {
    return {
      name: "zoe-bot",
      stage: "dev",
      region: config.aws_region,
    };
  },
  stacks(app) {
    app.stack(InfraStack).stack(BotStack).stack(WebStack);
  },
} satisfies SSTConfig;
