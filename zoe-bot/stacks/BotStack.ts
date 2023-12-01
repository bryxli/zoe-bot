import { Function, StackContext, use } from "sst/constructs";
import { InfraStack } from "./InfraStack";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as events from "aws-cdk-lib/aws-events";
import * as cdk from "aws-cdk-lib";
import * as targets from "aws-cdk-lib/aws-events-targets";
import * as config from "../config.json";

export function BotStack({ stack }: StackContext) {
  const { table } = use(InfraStack);

  const dynamoLayer = new lambda.LayerVersion(stack, "util-dynamo-layer", {
    code: lambda.Code.fromAsset("packages/functions/layers/dynamo"),
  });

  const leagueLayer = new lambda.LayerVersion(stack, "util-league-layer", {
    code: lambda.Code.fromAsset("packages/functions/layers/league"),
  });

  /* 
  const registerLayer = new lambda.LayerVersion(
    stack,
    "function-register-layer", {
      code: lambda.Code.fromAsset("packages/functions/layers/register"),
    },
  );

  const mainLayer = new lambda.LayerVersion(stack, "function-main-layer", {
    code: lambda.Code.fromAsset("packages/functions/layers/main"),
  });

  const taskLayer = new lambda.LayerVersion(stack, "function-task-layer", {
    code: lambda.Code.fromAsset("packages/functions/layers/task"),
  });
  */

  const registerFunction = new Function(stack, "function-register", {
    handler: "packages/functions/src/register/main.handler",
    runtime: "python3.9",
    memorySize: 1024,
    timeout: "5 minutes",
    architecture: "x86_64",
    environment: {
        TOKEN: config.token,
        APPLICATION_ID: config.application_id,
    },
  });

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
    },
    bind: [table],
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
    },
    bind: [table],
  });

  const taskRule = new events.Rule(stack, "function-task-rule", {
    schedule: events.Schedule.rate(cdk.Duration.minutes(5)),
  }).addTarget(new targets.LambdaFunction(taskFunction));

  const mainUrl = mainFunction.addFunctionUrl({
    authType: lambda.FunctionUrlAuthType.NONE,
    cors: {
      allowedOrigins: ["*"],
      allowedMethods: [lambda.HttpMethod.ALL],
      allowedHeaders: ["*"],
    },
  });

  stack.addOutputs({
    value: mainUrl.url,
  });

  /*
  // TODO: this event is not triggering upon CloudFormation deployment
    new events.Rule(this, "ZoeBotUploadRule", {
      eventPattern: {
        source: ["aws.cloudformation"],
        detailType: [
          "AWS CloudFormation Stack Creation Complete",
          "AWS CloudFormation Stack Update Complete",
        ],
        resources: [this.stackId],
      },
    }).addTarget(new targets.LambdaFunction(lambdaRegister)); 
  */
}
