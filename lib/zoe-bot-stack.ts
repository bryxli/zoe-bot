import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';

import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';

import * as iam from 'aws-cdk-lib/aws-iam';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as fs from 'fs'

export class ZoeBotStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Create DynamoDB table
    const table = new dynamodb.Table(this, 'ZoeBotTable', {
      partitionKey: { name: 'guild_id', type: dynamodb.AttributeType.NUMBER },
      // removalPolicy: cdk.RemovalPolicy.DESTROY,
      tableName: 'ZoeBotTable'
    });

    // Create EC2 role
    const iamRole = new iam.Role(this, 'ZoeBotIam', {
      assumedBy: new iam.ServicePrincipal('ec2.amazonaws.com')
    });

    // Create policy to access DynamoDB table
    const dynamoDbPolicy = new iam.ManagedPolicy(this, 'ZoeBotPolicy', {
      statements: [
        new iam.PolicyStatement({
          actions: [
            'dynamodb:Scan',
            'dynamodb:GetItem',
            'dynamodb:PutItem',
            'dynamodb:DeleteItem',
            'dynamodb:UpdateItem',
          ],
          resources: [
            table.tableArn
          ]
        })
      ]
    });

    // Attach SSM and DynamoDB access to EC2 role
    iamRole.addManagedPolicy(iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonSSMManagedInstanceCore'));
    iamRole.addManagedPolicy(dynamoDbPolicy);

    // Create VPC
    const vpc = new ec2.Vpc(this, 'ZoeBotVpc', {
      natGateways: 0,
      subnetConfiguration: [
        {
          name: 'public',
          subnetType: ec2.SubnetType.PUBLIC,
        },
      ],
    });

    // Create EC2 security group
    const securityGroup = new ec2.SecurityGroup(this, 'ZoeBotSg', {
      vpc: vpc,
      securityGroupName: 'ZoeBotSg',
    });
    securityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(22));

    // Create userData
    const userDataScript = fs.readFileSync('./startup.sh', 'utf8');
    const userData = ec2.UserData.forLinux();
    userData.addCommands(userDataScript);

    // Create EC2 instance
    const ec2Instance = new ec2.Instance(this,'ZoeBotInstance', {
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.T2, ec2.InstanceSize.MICRO),
      machineImage: new ec2.AmazonLinuxImage(),
      vpc: vpc,
      securityGroup: securityGroup,
      role: iamRole,
      userData: userData,
    });

    // Export EC2 instance id
    new cdk.CfnOutput(this, 'id', { value: ec2Instance.instanceId });
  }
}
