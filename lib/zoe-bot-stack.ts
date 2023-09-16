import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";

import * as lambda from "aws-cdk-lib/aws-lambda";

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
          DISCORD_PUBLIC_KEY: "fde7a11dc5c641dc8d51fada6f7d1f43055a5ac223b16d657fa92dc86b1600dc",
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