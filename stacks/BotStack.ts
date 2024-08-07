import { Function, StackContext, use } from "sst/constructs";
import { InfraStack } from "./InfraStack";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as events from "aws-cdk-lib/aws-events";
import * as cdk from "aws-cdk-lib";
import * as targets from "aws-cdk-lib/aws-events-targets";
import * as triggers from "aws-cdk-lib/triggers";
import * as config from "../configs/config.json";

export function BotStack({ app, stack }: StackContext) {
  const { table, dynamoLayer, leagueLayer } = use(InfraStack);

  const functionCode = lambda.Code.fromAsset(
    "packages/functions/src/register",
    {
      bundling: {
        image: lambda.Runtime.PYTHON_3_9.bundlingImage,
        command: [
          "bash",
          "-c",
          "cp -R /asset-input/* /asset-output/ && pip install -r requirements.txt -t /asset-output/",
        ],
      },
    },
  );

  const registerFunction = new triggers.TriggerFunction(
    stack,
    "function-register",
    {
      code: functionCode,
      handler: "main.handler",
      runtime: lambda.Runtime.PYTHON_3_9,
      memorySize: 1024,
      timeout: cdk.Duration.minutes(5),
      architecture: lambda.Architecture.X86_64,
      environment: {
        TOKEN: config.token,
        APPLICATION_ID: config.application_id,
      },
    },
  );

  const mainFunction = new Function(stack, "function-main", {
    handler: "packages/functions/src/main/main.handler",
    runtime: "python3.9",
    layers: [dynamoLayer, leagueLayer],
    memorySize: 1024,
    timeout: "5 minutes",
    architecture: "x86_64",
    environment: {
      DISCORD_PUBLIC_KEY: config.discord_public_key,
      RIOT_KEY: config.riot_key,
      SET_AWS_REGION: config.aws_region,
      TOKEN: config.token,
      STAGE: app.stage,
    },
    bind: [table],
    url: {
      authorizer: "none",
      cors: {
        allowOrigins: ["*"],
        allowMethods: [lambda.HttpMethod.ALL],
        allowHeaders: ["*"],
      },
    },
  });

  const taskFunction = new Function(stack, "function-task", {
    handler: "packages/functions/src/task/main.handler",
    runtime: "python3.9",
    layers: [dynamoLayer, leagueLayer],
    memorySize: 1024,
    timeout: "5 minutes",
    architecture: "x86_64",
    environment: {
      RIOT_KEY: config.riot_key,
      SET_AWS_REGION: config.aws_region,
      STAGE: app.stage,
    },
    bind: [table],
  });

  if (app.stage === "prod") {
    new events.Rule(stack, "function-task-rule", {
      schedule: events.Schedule.rate(cdk.Duration.minutes(5)),
    }).addTarget(new targets.LambdaFunction(taskFunction));

    new events.Rule(stack, "function-main-rule", {
      schedule: events.Schedule.rate(cdk.Duration.minutes(15)),
    }).addTarget(new targets.LambdaFunction(mainFunction));
  }

  stack.addOutputs({
    InteractionsEndpoint: mainFunction.url,
  });
}
