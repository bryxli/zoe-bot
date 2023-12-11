import { SummonerProps } from "@/app/types";

export const findByAccountId = async (
  accountId: string,
): Promise<SummonerProps> => {
  return {
    name: `dummy-${accountId.substring(0, 3)}`,
  };
};
