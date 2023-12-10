import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocument } from "@aws-sdk/lib-dynamodb";

const stage = "prod"; // Currently UI only deploys to prod, using process.env.STAGE results in undefined being rendered

const client = new DynamoDBClient();
const documentClient = DynamoDBDocument.from(client);

export const getAll = async () => {
  const res = await documentClient.scan({
    TableName: `${stage}-zoe-bot-db`,
  });

  return res.Items ?? [];
};

export const getGuild = async (guildId: string) => {
  const res = await documentClient.get({
    TableName: `${stage}-zoe-bot-db`,
    Key: { guild_id: BigInt(guildId) },
  });

  return res.Item ?? {};
};

// refactor this to use output of getguild
export const getAllUsers = async (guildId: string) => {
  const item = await getGuild(guildId);
  const userlist = item.userlist || [];
  let userIds: string[] = [];
  userlist.forEach((user: any) => {
    const accountId = Object.keys(user)[0];
    userIds.push(accountId);
  });

  return userIds;
};
