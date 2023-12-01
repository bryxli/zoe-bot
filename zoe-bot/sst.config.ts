import { SSTConfig } from "sst";
import { InfraStack } from "./stacks/InfraStack";
import { BotStack } from "./stacks/BotStack";

export default {
  config(_input) {
    return {
      name: "zoe-bot",
      stage: "dev",
      region: "us-east-1", // use region in config
    };
  },
  stacks(app) {
    app.stack(InfraStack).stack(BotStack);
  },
} satisfies SSTConfig;
