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

    const ami = new ec2.WindowsImage(ec2.WindowsVersion.WINDOWS_SERVER_2022_ENGLISH_CORE_BASE)

    const ec2Instance = new ec2.Instance(this,'ZoeBotInstance', {
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
      machineImage: ami,
      vpc: vpc,
      securityGroup: securityGroup,
      role: iamRole,
    });

    new cdk.CfnOutput(this, 'id == ', { value: ec2Instance.instanceId });    
  }
}
