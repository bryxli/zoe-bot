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
        layers: [dynamoLayer],
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
      "POST /guild/setup": {
        function: {
          handler: "packages/functions/src/api/guild/setup.handler",
          layers: [apiLayer],
        },
      },
      "POST /guild/region": "packages/functions/src/api/guild/region.handler",
      "POST /guild/reset": {
        function: {
          handler: "packages/functions/src/api/guild/delete.handler",
          layers: [apiLayer],
        },
      },
      "POST /guild/acknowledge":
        "packages/functions/src/api/guild/acknowledge.handler",
      "POST /league/account": {
        function: {
          handler: "packages/functions/src/api/league/add.handler",
          layers: [leagueLayer],
        },
      },
      "DELETE /league/account": {
        function: {
          handler: "packages/functions/src/api/league/delete.handler",
          layers: [leagueLayer],
        },
      },
      "GET /league/userlist": {
        function: {
          handler: "packages/functions/src/api/league/userlist.handler",
          layers: [leagueLayer],
        },
      },
    },
  });

  return {
    table,
    dynamoLayer,
    leagueLayer,
    apiURL: api.url,
  };
}
