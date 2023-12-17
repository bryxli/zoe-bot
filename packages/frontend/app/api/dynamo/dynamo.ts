import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocument } from "@aws-sdk/lib-dynamodb";

import { DynamoGuildProps } from "@/app/types";

const stage = "prod"; // Currently UI only deploys to prod, using process.env.STAGE results in undefined being rendered

const client = new DynamoDBClient();
const documentClient = DynamoDBDocument.from(client);

const defaultProps: DynamoGuildProps = {
  acknowledgment: false,
  guild_id: "",
  region: "",
  userlist: [],
  webhook_id: "",
  webhook_url: "",
};

export const getAll = async () => {
  const res = await documentClient.scan({
    TableName: `${stage}-zoe-bot-db`,
  });

  return res.Items ?? [];
};

export const getGuild = async (guildId: string): Promise<DynamoGuildProps> => {
  const res = await documentClient.get({
    TableName: `${stage}-zoe-bot-db`,
    Key: { guild_id: BigInt(guildId) },
  });

  return res.Item
    ? { ...defaultProps, ...res.Item }
    : {
        acknowledgment: false,
        guild_id: guildId,
        region: "",
        userlist: [],
        webhook_id: "",
        webhook_url: "",
      };
};

// adduser

// deluser

// region

export const createGuild = async (
  guildId: string,
  webhookId: string,
  webhookUrl: string,
): Promise<DynamoGuildProps> => {
  try {
    await documentClient.put({
      TableName: `${stage}-zoe-bot-db`,
      Item: {
        acknowledgment: false,
        guild_id: BigInt(guildId),
        region: "NA",
        userlist: [],
        webhook_id: webhookId,
        webhook_url: webhookUrl,
      },
    });
  } catch (e) {
    return defaultProps;
  }

  return {
    acknowledgment: false,
    guild_id: guildId,
    region: "NA",
    userlist: [],
    webhook_id: webhookId,
    webhook_url: webhookUrl,
  };
};

export const destroyGuild = async (
  guild: DynamoGuildProps,
): Promise<DynamoGuildProps> => {
  try {
    await documentClient.delete({
      TableName: `${stage}-zoe-bot-db`,
      Key: { guild_id: BigInt(guild.guild_id) },
    });
  } catch (e) {
    return guild;
  }

  return defaultProps;
};

export const acknowledge = async (
  guild: DynamoGuildProps,
): Promise<DynamoGuildProps> => {
  try {
    await documentClient.put({
      TableName: `${stage}-zoe-bot-db`,
      Item: {
        acknowledgment: true,
        guild_id: BigInt(guild.guild_id),
        region: guild.region,
        userlist: guild.userlist,
        webhook_id: guild.webhook_id,
        webhook_url: guild.webhook_url,
      },
    });

    guild.acknowledgment = true;
  } catch (e) {}

  return guild;
};
