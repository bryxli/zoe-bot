import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocument } from "@aws-sdk/lib-dynamodb";

import { DynamoGuildProps } from "@/app/types";

const stage = "prod"; // Currently UI only deploys to prod, using process.env.STAGE results in undefined being rendered

const client = new DynamoDBClient();
const documentClient = DynamoDBDocument.from(client);

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

  const defaultProps: DynamoGuildProps = {
    acknowledgment: false,
    guild_id: "",
    region: "",
    userlist: [],
    webhook_id: "",
    webhook_url: "",
  };

  return res.Item ? { ...defaultProps, ...res.Item } : defaultProps;
};

// adduser

// deluser

// region

export const destroyGuild = async (guild: DynamoGuildProps) => {
  // TODO: implement into commands component, check acknowledgment first
  try {
    await documentClient.delete({
      TableName: `${stage}-zoe-bot-db`,
      Key: { guild_id: BigInt(guild.guild_id) },
    });
  } catch (e) {
    console.log(e);
  }
};

export const acknowledge = async (guild: DynamoGuildProps) => {
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

    return guild;
  } catch (e) {}
};
