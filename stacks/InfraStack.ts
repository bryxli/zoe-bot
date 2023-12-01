import { StackContext, Table } from "sst/constructs";

export function InfraStack({ stack }: StackContext) {
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
