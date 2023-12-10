import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocument } from "@aws-sdk/lib-dynamodb";

import { DynamoGuildProps } from "../../types";

const stage = "prod"; // Currently UI only deploys to prod, using process.env.STAGE results in undefined being rendered

const client = new DynamoDBClient();
const documentClient = DynamoDBDocument.from(client);

export const getAll = async () => {
  const res = await documentClient.scan({
    TableName: `${stage}-zoe-bot-db`,
  });

  return res.Items ?? [];
};

// adduser

// deluser

// region

export const destroyGuild = async (guildId: string) => {
  // TODO: implement into commands component, check acknowledgment first
  try {
    await documentClient.delete({
      TableName: `${stage}-zoe-bot-db`,
      Key: { guild_id: guildId },
    });
  } catch (e) {}
};

// acknowledge

export const getGuild = async (guildId: string) => {
  const res = await documentClient.get({
    TableName: `${stage}-zoe-bot-db`,
    Key: { guild_id: BigInt(guildId) },
  });

  return res.Item ?? {};
};

// current webhook location

// current region location

// # of registered players

export const getAllUsers = async (guild: DynamoGuildProps) => {
  const userlist = guild.userlist || [];
  let userIds: string[] = [];
  userlist.forEach((user: any) => {
    const accountId = Object.keys(user)[0];
    userIds.push(accountId);
  });

  return userIds;
};
