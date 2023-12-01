import { Function, StackContext, use } from "sst/constructs";
import { InfraStack } from "./InfraStack";
import * as lambda from "aws-cdk-lib/aws-lambda";

export function BotStack({ stack }: StackContext) {
  const { table } = use(InfraStack);

  const registerLayer = new lambda.LayerVersion(
    stack,
    "function-register-layer",
    {
      code: lambda.Code.fromAsset("packages/functions/layers/register-layer"),
    },
  );

  const registerFunction = new Function(stack, "function-register", {
    handler: "packages/functions/src/register/main.handler",
    runtime: "python3.9",
    layers: [registerLayer],
    memorySize: 1024,
    timeout: "5 minutes",
    architecture: "x86_64",
    environment: {
      TOKEN:
        "MTE1NDY0NzA3MjEzODYwODY5NA.GiX8ea.5u0byyxcaBoAgH05WgktGjg3o8I2lsjEatzy-8",
      APPLICATION_ID: "1154647072138608694",
    },
  });
}
