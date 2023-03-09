import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as iam from 'aws-cdk-lib/aws-iam';

export class ZoeBotStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const vpc = new ec2.Vpc(this, 'ZoeBotVpc', {
      natGateways: 0,
      subnetConfiguration: [
        {
          name: 'public',
          subnetType: ec2.SubnetType.PUBLIC,
        },
      ],
    });

    const dynamo = new dynamodb.Table(this, 'ZoeBotTable', {
      partitionKey: { name: 'guild_id', type: dynamodb.AttributeType.NUMBER },
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const securityGroup = new ec2.SecurityGroup(this, 'ZoeBotSg', {
      vpc: vpc,
      securityGroupName: 'ZoeBotSg',
    });
    securityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(22), 'allow SSH access from anywhere');

    const iamRole = new iam.Role(this, 'ZoeBotIam', {
      assumedBy: new iam.ServicePrincipal('ec2.amazonaws.com')
    });
    iamRole.addManagedPolicy(iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonSSMManagedInstanceCore'));
    dynamo.grantReadWriteData(iamRole);

    /*
    const script = `#!/bin/bash
      yum install -y https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm
      systemctl start amazon-ssm-agent
    `;
    const userData = ec2.UserData.forLinux()
    userData.addCommands(script);
    */

    const ec2Instance = new ec2.Instance(this,'ZoeBotInstance', {
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
      machineImage: new ec2.AmazonLinuxImage(),
      vpc: vpc,
      securityGroup: securityGroup,
      role: iamRole,
      // userData: userData,
    });
  }
}
