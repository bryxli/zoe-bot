// this is the general structure of what this route would look like

import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import {
  DynamoDBDocumentClient,
  GetCommand,
  PutCommand,
  UpdateCommand,
} from "@aws-sdk/lib-dynamodb";

const stage = "prod"; // Currently UI only deploys to prod, using process.env.STAGE results in undefined being rendered

const dynamo = new DynamoDBClient({});
const client = DynamoDBDocumentClient.from(dynamo);

export const getAllUsers = async (guildId: string) => {
  const command = new GetCommand({
    TableName: `${stage}-zoe-bot-db`,
    Key: { guild_id: guildId },
  });

  try {
    console.log(`${stage}-zoe-bot-db`);
    const response = await client.send(command);
    console.log(response);

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
