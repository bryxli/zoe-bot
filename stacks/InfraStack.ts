import { Api, StackContext, Table } from "sst/constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as config from "../configs/config.json";

export function InfraStack({ app, stack }: StackContext) {
  app.stage !== "prod" && app.setDefaultRemovalPolicy("destroy");

  const table = new Table(stack, "db", {
    fields: {
      guild_id: "number",
    },
    primaryIndex: { partitionKey: "guild_id" },
  });

  const dynamoLayer = new lambda.LayerVersion(stack, "util-dynamo-layer", {
    code: lambda.Code.fromAsset("packages/functions/src/layers/dynamo", {
      bundling: {
        image: lambda.Runtime.PYTHON_3_9.bundlingImage,
        command: [
          "bash",
          "-c",
          "cp -R /asset-input/* /asset-output/ && pip install -r requirements.txt -t /asset-output/python/",
        ],
      },
    }),
  });

  const leagueLayer = new lambda.LayerVersion(stack, "util-league-layer", {
    code: lambda.Code.fromAsset("packages/functions/src/layers/league", {
      bundling: {
        image: lambda.Runtime.PYTHON_3_9.bundlingImage,
        command: [
          "bash",
          "-c",
          "cp -R /asset-input/* /asset-output/ && pip install -r requirements.txt -t /asset-output/python/",
        ],
      },
    }),
  });

  const apiLayer = new lambda.LayerVersion(stack, "util-api-layer", {
    code: lambda.Code.fromAsset("packages/functions/src/layers/api", {
      bundling: {
        image: lambda.Runtime.PYTHON_3_9.bundlingImage,
        command: [
          "bash",
          "-c",
          "cp -R /asset-input/* /asset-output/ && pip install -r requirements.txt -t /asset-output/python/",
        ],
      },
    }),
  });

  const api = new Api(stack, "api", {
    defaults: {
      function: {
        runtime: "python3.9",
        layers: [apiLayer, dynamoLayer, leagueLayer],
        permissions: [table],
        memorySize: 1024,
        timeout: "5 minutes",
        architecture: "x86_64",
        environment: {
          DISCORD_PUBLIC_KEY: config.discord_public_key,
          RIOT_KEY: config.riot_key,
          SET_AWS_REGION: config.aws_region,
          TOKEN: config.token,
          STAGE: app.stage,
          API_KEY: config.api_key,
        },
      },
    },
    routes: {
      "GET /guild": "packages/functions/src/api/guild/get.handler",
      "POST /guild/setup": "packages/functions/src/api/guild/setup.handler",
      "POST /guild/region": "packages/functions/src/api/guild/region.handler",
      "POST /guild/reset": "packages/functions/src/api/guild/delete.handler",
      "POST /guild/acknowledge":
        "packages/functions/src/api/guild/acknowledge.handler",
      "POST /league/account": "packages/functions/src/api/league/add.handler",
      "DELETE /league/account":
        "packages/functions/src/api/league/delete.handler",
      "GET /league/userlist":
        "packages/functions/src/api/league/userlist.handler",
    },
  });

  return {
    table,
    dynamoLayer,
    leagueLayer,
    apiURL: api.url,
  };
}
