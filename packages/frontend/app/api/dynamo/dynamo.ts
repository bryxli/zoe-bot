import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocument } from "@aws-sdk/lib-dynamodb";

const stage = "prod"; // Currently UI only deploys to prod, using process.env.STAGE results in undefined being rendered
const region = "us-east-1"; // process.env.AWS_REGION

const client = new DynamoDBClient({
  region: region, // may not be necessary (not needed locally)
});
const documentClient = DynamoDBDocument.from(client);

export const getAllUsers = async (guildId: string) => {
  try {
    const res = await documentClient.get({
      TableName: `${stage}-zoe-bot-db`,
      Key: { guild_id: BigInt(guildId) },
    });
    const userlist = res.Item?.userlist || [];
    let userIds: string[] = [];
    userlist.forEach((user: any) => {
      const accountId = Object.keys(user)[0];
      userIds.push(accountId);
    });

    return userIds;
  } catch (e) {
    return [];
  }
};
