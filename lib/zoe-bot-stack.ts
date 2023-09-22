import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";

import * as dynamodb from "aws-cdk-lib/aws-dynamodb";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as events from "aws-cdk-lib/aws-events";
import * as targets from "aws-cdk-lib/aws-events-targets";

import * as config from "../config.json";

export class ZoeBotStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const table = new dynamodb.Table(this, "ZoeBotTable", {
      partitionKey: { name: "guild_id", type: dynamodb.AttributeType.NUMBER },
      // removalPolicy: cdk.RemovalPolicy.DESTROY,
      tableName: "ZoeBotTable",
    });

    const registerLayer = new lambda.LayerVersion(this, "ZoeRegisterLayer", {
      code: lambda.Code.fromAsset("./src/layers/lambdaRegister"),
      compatibleRuntimes: [lambda.Runtime.PYTHON_3_9],
    });

    const mainLayer = new lambda.LayerVersion(this, "ZoeMainLayer", {
      code: lambda.Code.fromAsset("./src/layers/lambdaMain"),
      compatibleRuntimes: [lambda.Runtime.PYTHON_3_9],
    });

    const taskLayer = new lambda.LayerVersion(this, "ZoeTaskLayer", {
      code: lambda.Code.fromAsset("./src/layers/lambdaTask"),
      compatibleRuntimes: [lambda.Runtime.PYTHON_3_9],
    });

    const dynamoLayer = new lambda.LayerVersion(this, "ZoeDynamoLayer", {
      code: lambda.Code.fromAsset("./src/layers/dynamo"),
      compatibleRuntimes: [lambda.Runtime.PYTHON_3_9],
    });

    const leagueLayer = new lambda.LayerVersion(this, "ZoeLeagueLayer", {
      code: lambda.Code.fromAsset("./src/layers/league"),
      compatibleRuntimes: [lambda.Runtime.PYTHON_3_9],
    });

    const lambdaRegister = new lambda.Function(this, "ZoeFunctionRegister", {
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: "main.handler",
      code: lambda.Code.fromAsset("./src/register"),
      memorySize: 1024,
      timeout: cdk.Duration.minutes(5),
      architecture: lambda.Architecture.X86_64,
      environment: {
        TOKEN: config.token,
        APPLICATION_ID: config.application_id,
      },
      layers: [registerLayer],
    });

    const lambdaMain = new lambda.Function(this, "ZoeFunctionMain", {
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: "main.handler",
      code: lambda.Code.fromAsset("./src/main"),
      memorySize: 1024,
      timeout: cdk.Duration.seconds(10),
      architecture: lambda.Architecture.X86_64,
      environment: {
        DISCORD_PUBLIC_KEY: config.discord_public_key,
        RIOT_KEY: config.riot_key,
        SET_AWS_REGION: config.aws_region,
        TOKEN: config.token,
      },
      layers: [mainLayer, dynamoLayer, leagueLayer],
    });

    const lambdaTask = new lambda.Function(this, "ZoeFunctionTask", {
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: "main.handler",
      code: lambda.Code.fromAsset("./src/task"),
      memorySize: 1024,
      timeout: cdk.Duration.seconds(10),
      architecture: lambda.Architecture.X86_64,
      environment: {
        RIOT_KEY: config.riot_key,
        SET_AWS_REGION: config.aws_region,
      },
      layers: [taskLayer, dynamoLayer, leagueLayer],
    });

    table.grantFullAccess(lambdaMain);
    table.grantFullAccess(lambdaTask);

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

    new events.Rule(this, "ZoeBotTaskRule", {
      schedule: events.Schedule.rate(cdk.Duration.minutes(5)),
    }).addTarget(new targets.LambdaFunction(lambdaTask));

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
