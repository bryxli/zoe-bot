import { LolApi, Constants } from "twisted";

import { SummonerProps } from "@/types";

const api = new LolApi();

const regions = {
  BR: Constants.Regions.BRAZIL,
  EUNE: Constants.Regions.EU_EAST,
  EUW: Constants.Regions.EU_WEST,
  JP: Constants.Regions.JAPAN,
  KR: Constants.Regions.KOREA,
  LAN: Constants.Regions.LAT_NORTH,
  LAS: Constants.Regions.LAT_SOUTH,
  NA: Constants.Regions.AMERICA_NORTH,
  OCE: Constants.Regions.OCEANIA,
  TR: Constants.Regions.TURKEY,
  RU: Constants.Regions.RUSSIA,
};

export const findByAccountId = async (
  accountId: string,
  region: string,
): Promise<SummonerProps> => {
  // eslint-disable-next-line testing-library/no-await-sync-queries
  const res = await api.Summoner.getByAccountID(
    accountId,
    regions[region as keyof typeof regions],
  );

  return res.response;
};
