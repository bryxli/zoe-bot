import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";

import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as events from "aws-cdk-lib/aws-events";
import * as targets from "aws-cdk-lib/aws-events-targets";

import * as config from '../config.json'

export class ZoeBotStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const table = new dynamodb.Table(this, 'ZoeBotTable', {
      partitionKey: { name: 'guild_id', type: dynamodb.AttributeType.NUMBER },
      // removalPolicy: cdk.RemovalPolicy.DESTROY,
      tableName: 'ZoeBotTable'
    });

    const lambdaMain = new lambda.DockerImageFunction(
      this,
      "ZoeFunctionMain",
      {
        code: lambda.DockerImageCode.fromImageAsset("./src/main"),
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

    const lambdaTask = new lambda.DockerImageFunction(
      this,
      "ZoeFunctionTask",
      {
        code: lambda.DockerImageCode.fromImageAsset("./src/task"),
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
    
    table.grantFullAccess(lambdaMain);
    table.grantFullAccess(lambdaTask);

    const rule = new events.Rule(this, 'ZoeBotRule', {
      schedule: events.Schedule.rate(cdk.Duration.minutes(5)),
    });

    rule.addTarget(new targets.LambdaFunction(lambdaTask));

    const ZoeUrl = lambdaMain.addFunctionUrl({
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