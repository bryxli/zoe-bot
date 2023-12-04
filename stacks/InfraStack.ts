import { StackContext, Table } from "sst/constructs";

export function InfraStack({ app, stack }: StackContext) {
  app.stage !== "prod" && app.setDefaultRemovalPolicy("destroy");

  const table = new Table(stack, "db", {
    fields: {
      guild_id: "number",
    },
    primaryIndex: { partitionKey: "guild_id" },
  });

  return {
    table,
  };
}
