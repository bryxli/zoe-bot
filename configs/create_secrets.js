const { Octokit } = require("@octokit/core");
const sodium = require("libsodium-wrappers");
const config = require("./config.actions.json");

const pat = config.pat;
const owner = config.owner;
const repo = config.repo;

const accountId = config.aws_account_id;
const region = config.aws_region;
const riotKey = config.riot_key;

const octokit = new Octokit({
  auth: pat,
});

const getRepo = async () => {
  return await octokit.request("GET /repos/{owner}/{repo}", {
    owner: owner,
    repo: repo,
    headers: {
      "X-GitHub-Api-Version": "2022-11-28",
    },
  });
};

const getPublicKey = async () => {
  return await octokit.request(
    "GET /repos/{owner}/{repo}/actions/secrets/public-key",
    {
      owner: owner,
      repo: repo,
      headers: {
        "X-GitHub-Api-Version": "2022-11-28",
      },
    },
  );
};

const getDependabotPublicKey = async () => {
  return await octokit.request(
    "GET /repos/{owner}/{repo}/dependabot/secrets/public-key",
    {
      owner: owner,
      repo: repo,
      headers: {
        "X-GitHub-Api-Version": "2022-11-28",
      },
    },
  );
};

const encrypt = async (key, secret) => {
  return new Promise((resolve) => {
    sodium.ready.then(() => {
      const binkey = sodium.from_base64(key, sodium.base64_variants.ORIGINAL);
      const binsec = sodium.from_string(secret);
      const encBytes = sodium.crypto_box_seal(binsec, binkey);
      const encryptedValue = sodium.to_base64(
        encBytes,
        sodium.base64_variants.ORIGINAL,
      );
      resolve(encryptedValue);
    });
  });
};

const createEnvironment = async (environmentName) => {
  await octokit.request(
    "PUT /repos/{owner}/{repo}/environments/{environment_name}",
    {
      owner: owner,
      repo: repo,
      environment_name: environmentName,
      headers: {
        "X-GitHub-Api-Version": "2022-11-28",
      },
    },
  );
};

const createSecret = async (secretName, secret) => {
  const repoKey = await getPublicKey();
  const encryptedValue = await encrypt(repoKey.data.key, secret);

  await octokit.request(
    "PUT /repos/{owner}/{repo}/actions/secrets/{secret_name}",
    {
      owner: owner,
      repo: repo,
      secret_name: secretName,
      encrypted_value: encryptedValue,
      key_id: repoKey.data.key_id,
      headers: {
        "X-GitHub-Api-Version": "2022-11-28",
      },
    },
  );
};

const createDependabotSecret = async (secretName, secret) => {
  const repoKey = await getDependabotPublicKey();
  const encryptedValue = await encrypt(repoKey.data.key, secret);

  await octokit.request(
    "PUT /repos/{owner}/{repo}/dependabot/secrets/{secret_name}",
    {
      owner: owner,
      repo: repo,
      secret_name: secretName,
      encrypted_value: encryptedValue,
      key_id: repoKey.data.key_id,
      headers: {
        "X-GitHub-Api-Version": "2022-11-28",
      },
    },
  );
};

const createEnvSecret = async (
  // TODO: env secrets not containing value
  secretName,
  secret,
  repositoryId,
  environmentName,
) => {
  const repoKey = await getPublicKey();
  const encryptedValue = await encrypt(repoKey.data.key, secret);

  await octokit.request(
    "PUT /repositories/{repository_id}/environments/{environment_name}/secrets/{secret_name}",
    {
      repository_id: repositoryId,
      environment_name: environmentName,
      secret_name: secretName,
      encrypted_value: encryptedValue,
      key_id: repoKey.data.key_id,
      headers: {
        "X-GitHub-Api-Version": "2022-11-28",
      },
    },
  );
};

const createRepoSecrets = async () => {
  await createSecret("AWS_ACCOUNT_ID", accountId);
  await createSecret("AWS_REGION", region);
  await createSecret("RIOT_KEY", riotKey);
};

const createDependabotRepoSecrets = async () => {
  await createDependabotSecret("AWS_ACCOUNT_ID", accountId);
  await createDependabotSecret("AWS_REGION", region);
  await createDependabotSecret("RIOT_KEY", riotKey);
};

const createEnvSecrets = async (stage) => {
  const repoId = (await getRepo()).data.id;

  await createEnvironment(stage);
  await createEnvSecret(
    "DISCORD_PUBLIC_KEY",
    config[stage].discord_public_key,
    repoId,
    stage,
  );
  await createEnvSecret(
    "APPLICATION_ID",
    config[stage].application_id,
    repoId,
    stage,
  );
  await createEnvSecret("TOKEN", config[stage].token, repoId, stage);
};

const run = async () => {
  await createRepoSecrets();
  await createDependabotRepoSecrets();
  await createEnvSecrets("dev");
  await createEnvSecrets("prod");
};

run();
