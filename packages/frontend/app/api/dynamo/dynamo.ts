// this is the general structure of what this route would look like

import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import {
  DynamoDBDocument,
  GetCommand,
  PutCommand,
  UpdateCommand,
} from "@aws-sdk/lib-dynamodb";

const stage = "prod"; // Currently UI only deploys to prod, using process.env.STAGE results in undefined being rendered

const client = new DynamoDBClient({
  region: "us-east-1",
});
const documentClient = DynamoDBDocument.from(client);

export const getAllUsers = async (guildId: string) => {
  try {
    const res = await documentClient.get({
      TableName: `${stage}-zoe-bot-db`,
      Key: { guild_id: guildId },
    });
    const userlist = res.Item?.userlist?.L || [];
    const userIds: string[] = [];
    userlist.forEach((user: any) => {
      const accountIds = Object.keys(user.M || {});
      userIds.push(...accountIds);
    });

    return userIds;
  } catch (e) {
    console.log(e);
    return [];
  }
};
