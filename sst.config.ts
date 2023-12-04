import { SSTConfig } from "sst";
import { InfraStack } from "./stacks/InfraStack";
import { BotStack } from "./stacks/BotStack";
import { WebStack } from "./stacks/WebStack";
import * as config from "./configs/config.json";

export default {
  config(_input) {
    return {
      name: "zoe-bot",
      region: config.aws_region,
    };
  },
  stacks(app) {
    app.stack(InfraStack).stack(BotStack);
    app.stage !== "dev" && app.stack(WebStack); // Do not deploy to dev
  },
} satisfies SSTConfig;
