import { DynamoDB } from "aws-sdk";

const stage = process.env.STAGE;

const dynamo = new DynamoDB.DocumentClient();

export const getAllUsers = async (guildId: string) => {
  const params = {
    TableName: `${stage}-zoe-bot-db`,
    Key: { guild_id: guildId },
  };

  try {
    console.log("test running dynamo");
    const response = await dynamo.get(params).promise();
    const userlist = response.Item?.userlist?.L || [];
    const userIds: string[] = [];
    userlist.forEach((user: any) => {
      const accountIds = Object.keys(user.M || {});
      userIds.push(...accountIds);
    });

    return userIds;
  } catch (e) {
    console.error;
  }
};
