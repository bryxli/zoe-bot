import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";

import * as lambda from "aws-cdk-lib/aws-lambda";

import * as config from '../config.json'

export class ZoeBotStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const dockerFunction = new lambda.DockerImageFunction(
      this,
      "ZoeFunction",
      {
        code: lambda.DockerImageCode.fromImageAsset("./src"),
        memorySize: 1024,
        timeout: cdk.Duration.seconds(10),
        architecture: lambda.Architecture.X86_64,
        environment: {
          DISCORD_PUBLIC_KEY: config.discord_public_key,
          TOKEN: config.token,
          APPLICATION_ID: config.application_id,
          GUILD_ID: config.guild_id,
          RIOT_KEY: config.riot_key
        },
      }
    );

    const ZoeUrl = dockerFunction.addFunctionUrl({
      authType: lambda.FunctionUrlAuthType.NONE,
      cors: {
        allowedOrigins: ["*"],
        allowedMethods: [lambda.HttpMethod.ALL],
        allowedHeaders: ["*"],
      },
    });

    new cdk.CfnOutput(this, "ZoeUrl", {
      value: ZoeUrl.url,
    });
  }
}