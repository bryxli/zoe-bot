export const findByAccountId = async (accountId: string) => {
  return {
    name: `dummy-${accountId.substring(0, 3)}`,
  };
};
