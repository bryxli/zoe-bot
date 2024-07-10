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

  const api = new Api(stack, "api", {
    defaults: {
      function: {
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
      },
    },
    routes: {
      "GET /guild": "packages/functions/src/api/guild.get_guild",
      "POST /guild/setup": "packages/functions/src/api/guild.setup_guild",
      "POST /guild/region": "packages/functions/src/api/guild.change_region",
      "POST /guild/reset": "packages/functions/src/api/guild.delete_guild",
      "POST /guild/acknowledge": "packages/functions/src/api/guild.acknowledge",
      "GET /league": "packages/functions/src/api/league.get_user",
      "POST /league/account": "packages/functions/src/api/league.add_user",
      "DELETE /league/account": "packages/functions/src/api/league.delete_user",
    },
  });

  api.bind([table]);

  return {
    table,
    dynamoLayer,
    leagueLayer,
    apiURL: api.url,
  };
}
