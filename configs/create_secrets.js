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

const createSecret = async (repoKey, secretName, secret) => {
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

const createDependabotSecret = async (repoKey, secretName, secret) => {
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
  repoKey,
  secretName,
  secret,
  repositoryId,
  environmentName,
) => {
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

const createRepoSecrets = async (repoKey) => {
  await createSecret(repoKey, "AWS_ACCOUNT_ID", accountId);
  await createSecret(repoKey, "AWS_REGION", region);
  await createSecret(repoKey, "RIOT_KEY", riotKey);
};

const createDependabotRepoSecrets = async (repoKey) => {
  await createDependabotSecret(repoKey, "AWS_ACCOUNT_ID", accountId);
  await createDependabotSecret(repoKey, "AWS_REGION", region);
  await createDependabotSecret(repoKey, "RIOT_KEY", riotKey);
};

const createEnvSecrets = async (repoKey, stage) => {
  const repoId = (await getRepo()).data.id;

  await createEnvironment(stage);
  await createEnvSecret(
    repoKey,
    "DISCORD_PUBLIC_KEY",
    config[stage].discord_public_key,
    repoId,
    stage,
  );
  await createEnvSecret(
    repoKey,
    "APPLICATION_ID",
    config[stage].application_id,
    repoId,
    stage,
  );
  await createEnvSecret(repoKey, "TOKEN", config[stage].token, repoId, stage);
};

const run = async () => {
  const publicKey = await getPublicKey();
  const dependabotPublicKey = await getDependabotPublicKey();

  await createRepoSecrets(publicKey);
  await createDependabotRepoSecrets(dependabotPublicKey);
  await createEnvSecrets(publicKey, "dev");
  await createEnvSecrets(publicKey, "prod");
};

run();
