import os.path

from aws_cdk import (
    aws_dynamodb as dynamodb,
    aws_ec2 as ec2,
    aws_iam as iam,
    App, Stack, RemovalPolicy
)

from constructs import Construct

dirname = os.path.dirname(__file__)


class ZoeStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # VPC
        vpc = ec2.Vpc(self, "VPC",
                      nat_gateways=0,
                      subnet_configuration=[ec2.SubnetConfiguration(
                          name="public", subnet_type=ec2.SubnetType.PUBLIC)]
                      )

        # AMI
        amzn_linux = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
        )

        # Instance Role and SSM Managed Policy
        role = iam.Role(self, "zoe_role",
                        assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name(
            "AmazonSSMManagedInstanceCore"))
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess'))

        # Dynamo
        table = dynamodb.Table(
            self, "zoe_db",
            partition_key=dynamodb.Attribute(
                name="guild_id",
                type=dynamodb.AttributeType.NUMBER
            ),
            table_name="zoe_db",
            removal_policy=RemovalPolicy.DESTROY
        )

        table.grant_read_write_data(role)

        # Instance
        instance = ec2.Instance(self, "zoe_instance",
                                instance_type=ec2.InstanceType("t3.micro"),
                                machine_image=amzn_linux,
                                vpc=vpc,
                                role=role
                                )


app = App()
ZoeStack(app, "zoe-bot")

app.synth()
